from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
import models
import datetime

def possessionExplore(p_coin_list, bithumb, db):
  try:
    print("possessionExplore start ::: ::: ")
    for p_coin in p_coin_list:
      if p_coin.status == 1:
        order_desc = ['bid', p_coin.coin, p_coin.order_id, 'KRW']
        coin_order_status = bithumb.get_order_completed(order_desc)
        # print("possessionExplore coin_order_status ::: ::: ", coin_order_status)
        if coin_order_status['data']['order_status'] == 'Cancel':
          del_coin = db.query(models.possessionCoin).filter(models.possessionCoin.coin == p_coin.coin).first()
          print("del_coin ::: ::: ", del_coin)
          if del_coin == None: pass
          db.delete(del_coin)

        if coin_order_status['data']['order_status'] == 'Completed':
          had_coin = db.query(models.possessionCoin).filter(models.possessionCoin.coin == p_coin.coin).first()
          print("com_coin ::: ::: ", had_coin.coin)
          order_sum = {'unit': 0, 'total': 0, 'fee': 0}
          for cont in coin_order_status['data']['contract']:
              order_sum['unit'] += float(cont['units'])
              order_sum['total'] += float(cont['total'])
              order_sum['fee'] += float(cont['fee'])

          had_coin.unit = float(had_coin.unit) + order_sum['unit']
          print("had_coin.unit", had_coin.unit)
          had_coin.price = float(had_coin.price) + float(coin_order_status['data']['order_price'])
          had_coin.total = float(had_coin.total) + order_sum['total']
          had_coin.fee = float(had_coin.fee) + order_sum['fee']
          had_coin.status = 0
          had_coin.transaction_time = datetime.datetime.now()
          had_coin.trailingstop_flag = 0
          had_coin.max = had_coin.price
          db.commit()
          print("com_coin insert ::: ::: ")

        if coin_order_status['data']['order_status'] == 'Pending':
          order_sum = {'unit': 0, 'total': 0, 'fee': 0}
          if len(coin_order_status['data']['contract']) > 0:
              for cont in coin_order_status['data']['contract']:
                  order_sum['unit'] += float(cont['units'])
                  order_sum['total'] += float(cont['total'])
                  order_sum['fee'] += float(cont['fee'])
              order_sum['price'] = coin_order_status['data']['order_price']
              trading = db.query(models.possessionCoin).filter(
                  models.possessionCoin.coin == coin_order_status['data']['order_currency'])
              print("pen_coin ::: ::: ", trading.coin)
              trading.unit = order_sum['unit']
              trading.total = order_sum['total']
              trading.price = order_sum['price']
              trading.fee = order_sum['fee']
              db.commit()
    db.commit()
  except Exception as e:
    print("Error ::: :::", e)
    db.rollback()
