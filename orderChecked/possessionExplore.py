from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
import models

def possessionExplore(p_coin_list, bithumb, db):
  print("possessionExplore start ::: ::: ")
  for p_coin in p_coin_list:
    if p_coin.status == 1:
      print("possessionExplore p_coin pass if ::: ::: ", p_coin.coin)
      order_desc = ['bid', p_coin.coin, p_coin.order_id, 'KRW']
      coin_order_status = bithumb.get_order_completed(order_desc)
      print("possessionExplore coin_order_status ::: ::: ", coin_order_status)
      if coin_order_status['data']['order_status'] == 'Cancel':
        del_coin = db.query(models.possessionCoin).filter(
          models.possessionCoin.coin == p_coin.coin).first()
        print("del_coin ::: ::: ",del_coin)
        if del_coin == None: pass
        db.delete(del_coin)
  db.commit()