
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from pybithumb import Bithumb

# api url
url = 'http://192.168.10.43:8888'

secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"
bithumb = Bithumb(connenctKey, secretKey)

now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

orderList = db.query(models.orderCoin).all()
krTime = 60 * 60 * 9
# 주문 확인 매매 성공 확인, 취소
for order in orderList:
    # 매수 확인
    if order.status == 1:
        isOrder = []

        order_desc = ['bid',order.coin, order.order_id, 'KRW']
        orderStatus = bithumb.get_order_completed(order_desc)
        if orderStatus['data']['order_status'] == 'Completed':
            had_coin = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
            if had_coin == None:
                possession_coin = models.possessionCoin()
                possession_coin.coin = order.coin
                possession_coin.unit = orderStatus['data']['contract'][0]['units']
                possession_coin.price = orderStatus['data']['contract'][0]['price']
                possession_coin.total = orderStatus['data']['contract'][0]['total']
                possession_coin.fee = orderStatus['data']['contract'][0]['fee']
                possession_coin.status = 0
                possession_coin.transaction_time = order.transaction_time
                possession_coin.conclusion_time = datetime.datetime.now()
                possession_coin.order_id = '-'
                print(datetime.datetime.utcfromtimestamp(int(orderStatus['data']['contract'][0]['transaction_date'][:-6])), 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
                db.add(possession_coin)

                db.delete(order)

            else:
                had_coin.unit = float(had_coin.unit) + float(orderStatus['data']['contract'][0]['units'])
                had_coin.price = float(had_coin.price) + float(orderStatus['data']['contract'][0]['price'])
                had_coin.total = float(had_coin.total) + float(orderStatus['data']['contract'][0]['total'])
                had_coin.fee = float(had_coin.fee) + float(orderStatus['data']['contract'][0]['fee'])
                had_coin.status = 0
                had_coin.transaction_time = datetime.datetime.now()

                db.delete(order)

            transactionLog = models.possessionLog()
            transactionLog.coin = order.coin
            transactionLog.unit = orderStatus['data']['contract'][0]['units']
            transactionLog.price = orderStatus['data']['contract'][0]['price']
            transactionLog.total = orderStatus['data']['contract'][0]['total']
            transactionLog.fee = orderStatus['data']['contract'][0]['fee']
            transactionLog.status = 0
            transactionLog.transaction_time = order.transaction_time
            transactionLog.conclusion_time = datetime.datetime.now()
            transactionLog.type = 'bid'
            transactionLog.order_id = order.order_id
            db.add(transactionLog)

        if orderStatus['data']['order_status'] == 'Pending':
            print(datetime.datetime.utcfromtimestamp(int(orderStatus['data']['order_date'][:-6]) + krTime))
            timeCheck = str(datetime.datetime.strptime(order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
            print(timeCheck[0])
            if timeCheck[0] == '-':
                delpossession = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
                cancel = bithumb.cancel_order(order_desc)
                if cancel == True:
                    db.delete(order)
                    db.delete(delpossession)

        print(orderStatus)

        db.commit()

    # 매도 확인
    if order.status == 3 or order.status == 5:
        isOrder = []

        order_desc = ['ask',order.coin, order.order_id, 'KRW']
        orderStatus = bithumb.get_order_completed(order_desc)
        Possession = db.query(models.possessionCoin).filter(models.possessionCoin.coin == order.coin).first()
        if orderStatus['data']['order_status'] == 'Completed':
            poseesionCheck = db.query(models.orderCoin).filter(models.orderCoin.coin == order.coin).all()
            if len(poseesionCheck) == 1:
                db.delete(Possession)
            else:
                Possession.unit = float(Possession.unit) - float(orderStatus['data']['contract'][0]['units'])
                Possession.unit = float(Possession.price) - float(orderStatus['data']['contract'][0]['price'])
                Possession.unit = float(Possession.total) - float(orderStatus['data']['contract'][0]['total'])
                Possession.unit = float(Possession.fee) - float(orderStatus['data']['contract'][0]['fee'])
                Possession.transaction_time = order.transaction_time
            db.delete(order)

            transactionLog = models.possessionLog()
            transactionLog.coin = order.coin
            transactionLog.unit = orderStatus['data']['contract'][0]['units']
            transactionLog.price = orderStatus['data']['contract'][0]['price']
            transactionLog.total = orderStatus['data']['contract'][0]['total']
            transactionLog.fee = orderStatus['data']['contract'][0]['fee']
            transactionLog.status = 6
            transactionLog.transaction_time = order.transaction_time
            transactionLog.conclusion_time = datetime.datetime.now()
            transactionLog.type = 'ask'
            transactionLog.order_id = order.order_id
            db.add(transactionLog)

        if orderStatus['data']['order_status'] == 'Pending':
            timeCheck = str(datetime.datetime.strptime(order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
            print(timeCheck[0])
            if timeCheck[0] == '-':
                cancel = bithumb.cancel_order(order_desc)
                if cancel == True:
                    db.delete(order)
                    Possession.status = 4

        print(orderStatus)
        db.commit()

print('process end')