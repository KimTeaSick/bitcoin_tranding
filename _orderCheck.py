from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from pybithumb import Bithumb
from orderChecked.possessionExplore import possessionExplore
from orderChecked.buyCheck import BUY_CHECK

now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()


def orderCheck():
  try:
    db = SessionLocal()
    db: Session
    active_users = db.query(models.USER_T).all()
    for user in active_users:
      bithumb = Bithumb(user.public_key, user.secret_key)
      krTime = 60 * 60 * 9
      # 주문 확인 매매 성공 확인, 취소
      orderList = db.query(models.orderCoin).filter(models.orderCoin.user_idx == user.idx).all()
      for order in orderList:
          possession_list = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == user.idx).all()
          print("buy order status order_id ::: ::: ", order.order_id)
          # 매수 확인
          if order.status == 1:
              order_desc = ['bid', order.coin, order.order_id, 'KRW']
              orderStatus = bithumb.get_order_completed(order_desc)
              # BUY_CHECK(orderStatus, order, bithumb, db)
              print("buy order status ::: ::: ", orderStatus)
              print("--------------------------------------------------------------------------")

              if orderStatus['data']['order_status'] == 'Completed':
                  possession_coin_c = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
                  order_sum = {'unit': 0, 'total': 0, 'fee': 0}
                  for cont in orderStatus['data']['contract']:
                      order_sum['unit'] += float(cont['units'])
                      order_sum['total'] += float(cont['total'])
                      order_sum['fee'] += float(cont['fee'])
                  possession_coin_c.unit = float(possession_coin_c.unit) + order_sum['unit']
                  possession_coin_c.price = float(possession_coin_c.price) + orderStatus['data']['order_price']
                  possession_coin_c.total = float(possession_coin_c.total) + order_sum['total']
                  possession_coin_c.fee = float(possession_coin_c.fee) + order_sum['fee']
                  possession_coin_c.status = 0
                  possession_coin_c.transaction_time = datetime.datetime.now()
                  possession_coin_c.trailingstop_flag = 0
                  possession_coin_c.max = possession_coin_c.price
                  db.delete(order)

                  transaction_log = models.possessionLog()
                  transaction_log.coin = order.coin
                  transaction_log.unit = order_sum['unit']
                  transaction_log.price = orderStatus['data']['contract'][0]['price']
                  transaction_log.total = order_sum['total']
                  transaction_log.fee = order_sum['fee']
                  transaction_log.status = 0
                  transaction_log.transaction_time = order.transaction_time
                  transaction_log.conclusion_time = datetime.datetime.now()
                  transaction_log.type = 'bid'
                  transaction_log.order_id = order.order_id
                  transaction_log.user_idx = user.idx
                  db.add(transaction_log)

              if orderStatus['data']['order_status'] == 'Pending':
                  order_sum = {'unit': 0, 'total': 0, 'fee': 0}
                  if len(orderStatus['data']['contract']) > 0:
                      for cont in orderStatus['data']['contract']:
                          order_sum['unit'] += float(cont['units'])
                          order_sum['total'] += float(cont['total'])
                          order_sum['fee'] += float(cont['fee'])
                      order_sum['price'] = orderStatus['data']['order_price']
                      possession_list_p = db.query(models.possessionCoin).filter(
                          models.possessionCoin.coin == orderStatus['data']['order_currency'])
                      possession_list_p.unit = order_sum['unit']
                      possession_list_p.total = order_sum['total']
                      possession_list_p.price = order_sum['price']
                      possession_list_p.fee = order_sum['fee']
                      db.commit()

                  print(datetime.datetime.utcfromtimestamp(int(orderStatus['data']['order_date'][:-6]) + krTime))

                  timeCheck = str(datetime.datetime.strptime(order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())

                  print(timeCheck[0])

                  if timeCheck[0] == '-':
                    del_possession = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
                    # 분할매도에 완전히 실패할 경우 내역에서 제거하는 로직
                    cancel = bithumb.cancel_order(order_desc)
                    if cancel == True:
                      db.delete(order)
                      if len(orderStatus['data']['contract']) != 0:
                        db.delete(del_possession)
              db.commit()
              print("매수 주문 처리 완료 :::: ::::")

          # 매도 확인
          if order.status == 3 or order.status == 5:
              print("매도 주문 처리 시작 :::: ::::")
              sell_order_desc = ['ask', order.coin, order.order_id, 'KRW']
              orderStatus = bithumb.get_order_completed(sell_order_desc)
              Possession = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
              print("orderStatus ::: ::: ", orderStatus)
              if orderStatus == None : continue
              print("---------------------------------------------------------------------------------")

              if orderStatus['data']['order_status'] == 'Completed':
                  order_price: float = 0.0
                  order_sum = {'unit': 0, 'total': 0, 'fee': 0}
                  for sell_info in orderStatus['data']['contract']:
                      order_sum['unit'] += float(sell_info['units'])
                      order_sum['total'] += float(sell_info['total'])
                      order_sum['fee'] += float(sell_info['fee'])
                      order_price += float(sell_info["price"])
                  order_sum['price'] = order_price / len(orderStatus['data']['contract'])
                  db.delete(Possession)
                  db.delete(order)

                  for cont in orderStatus['data']['contract']:
                      print('cont', cont)

                  transactionLog = models.possessionLog()
                  transactionLog.coin = order.coin
                  transactionLog.unit = order_sum['unit']
                  transactionLog.price = order_sum['price']
                  transactionLog.total = order_sum['total']
                  transactionLog.fee = order_sum['fee']
                  transactionLog.status = 6
                  transactionLog.transaction_time = order.transaction_time
                  transactionLog.conclusion_time = datetime.datetime.now()
                  transactionLog.type = 'ask'
                  transactionLog.order_id = order.order_id
                  transactionLog.sell_reason = order.sell_reason
                  transactionLog.user_idx = user.idx
                  db.add(transactionLog)

              if orderStatus['data']['order_status'] == 'Pending':
                  order_sum = {'unit': 0, 'total': 0, 'fee': 0}
                  if len(orderStatus['data']['contract']) > 0:
                      for cont in orderStatus['data']['contract']:
                          order_sum['unit'] += float(cont['units'])
                          order_sum['total'] += float(cont['total'])
                          order_sum['fee'] += float(cont['fee'])
                      order_sum['price'] = orderStatus['data']['order_price']
                      trading = db.query(models.possessionCoin).filter(models.possessionCoin.coin == orderStatus['data']['order_currency']).first()
                      trading.unit = float(trading.unit) - order_sum['unit']
                      trading.total = float(trading.total) - order_sum['total']
                      trading.price = order_sum['price']
                      trading.fee = float(trading.fee) - order_sum['fee']
                      db.commit()

                  timeCheck = str(datetime.datetime.strptime(order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
                  print(timeCheck[0])
                  if timeCheck[0] == '-':
                      if len(orderStatus['data']['contract']) > 0:
                          if float(trading.total) < 1000:
                              continue
                      cancel = bithumb.cancel_order(sell_order_desc)
                      if cancel == True:
                          db.delete(order)
                          Possession.status = 4
              print("매도 주문 처리 완료 :::: ::::")
              db.commit()

          # possessionExplore(possession_list, bithumb, db)
      print('process end')
  finally:
    db.close()