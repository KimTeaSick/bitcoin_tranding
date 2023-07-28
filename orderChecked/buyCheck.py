import models
import datetime 

krTime = 60 * 60 * 9

def BUY_CHECK(orderStatus, order, bithumb, db):
  order_desc = ['bid', order.coin, order.order_id, 'KRW']

  if orderStatus['data']['order_status'] == 'Completed':
    had_coin = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
    order_sum = {'unit': 0, 'total': 0, 'fee': 0}
    for cont in orderStatus['data']['contract']:
        order_sum['unit'] += float(cont['units'])
        order_sum['total'] += float(cont['total'])
        order_sum['fee'] += float(cont['fee'])
    had_coin.unit = float(had_coin.unit) + order_sum['unit']
    had_coin.price = float(had_coin.price) + float(orderStatus['data']['order_price'])
    had_coin.total = float(had_coin.total) + order_sum['total']
    had_coin.fee = float(had_coin.fee) + order_sum['fee']
    had_coin.status = 0
    had_coin.transaction_time = datetime.datetime.now()
    had_coin.trailingstop_flag = 0
    had_coin.max = had_coin.price
    db.delete(order)
    transactionLog = models.possessionLog()
    transactionLog.coin = order.coin
    transactionLog.unit = order_sum['unit']
    transactionLog.price = orderStatus['data']['contract'][0]['price']
    transactionLog.total = order_sum['total']
    transactionLog.fee = order_sum['fee']
    transactionLog.status = 0
    transactionLog.transaction_time = order.transaction_time
    transactionLog.conclusion_time = datetime.datetime.now()
    transactionLog.type = 'bid'
    transactionLog.order_id = order.order_id
    db.add(transactionLog)
  if orderStatus['data']['order_status'] == 'Pending':
      order_sum = {'unit': 0, 'total': 0, 'fee': 0}
      if len(orderStatus['data']['contract']) > 0:
          for cont in orderStatus['data']['contract']:
              order_sum['unit'] += cont['units']
              order_sum['total'] += cont['total']
              order_sum['fee'] += cont['fee']
          order_sum['price'] = orderStatus['data']['order_price']
          trading = db.query(models.possessionCoin).filter(
              models.possessionCoin.coin == orderStatus['data']['order_currency'])
          trading.unit = order_sum['unit']
          trading.total = order_sum['total']
          trading.price = order_sum['price']
          trading.fee = order_sum['fee']
          db.commit()
      print(datetime.datetime.utcfromtimestamp(
          int(orderStatus['data']['order_date'][:-6]) + krTime))
      timeCheck = str(datetime.datetime.strptime(
          order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
      print(timeCheck[0])
      if timeCheck[0] == '-':
          delpossession = db.query(models.possessionCoin).filter(
              models.possessionCoin.coin == order.coin).first()
          # 분할매도에 완전히 실패할 경우 내역에서 제거하는 로직
          cancel = bithumb.cancel_order(order_desc)
          if cancel == True:
              db.delete(order)
              if len(orderStatus['data']['contract']) != 0:
                  db.delete(delpossession)
  print(orderStatus)
  db.commit()