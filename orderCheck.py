
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from pybithumb import Bithumb

secretKey = "ee7741a2e52957613c020ded3c91751c"
connenctKey = "ef3d9e8fb9b15ca740150fed18cdaaae"

bithumb = Bithumb(connenctKey, secretKey)

now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

autoStatus = db.query(models.autoTradingStatus).filter(
    models.autoTradingStatus.status == 1).first()

if autoStatus == None:
    print('자동 매매 정지 exit')
    exit()

orderList = db.query(models.orderCoin).all()
krTime = 60 * 60 * 9

# 주문 확인 매매 성공 확인, 취소
for order in orderList:
    # 매수 확인
    if order.status == 1:
        isOrder = []

        order_desc = ['bid', order.coin, order.order_id, 'KRW']
        orderStatus = bithumb.get_order_completed(order_desc)
        if orderStatus['data']['order_status'] == 'Completed':
            had_coin = db.query(models.possessionCoin).filter(
                models.possessionCoin.coin == order.coin).first()

            orderSum = {'unit': 0, 'total': 0, 'fee': 0}

            for cont in orderStatus['data']['contract']:
                orderSum['unit'] += float(cont['units'])
                orderSum['total'] += float(cont['total'])
                orderSum['fee'] += float(cont['fee'])

            had_coin.unit = float(
                had_coin.unit) + orderSum['unit']
            had_coin.price = float(
                had_coin.price) + float(orderStatus['data']['order_price'])
            had_coin.total = float(
                had_coin.total) + orderSum['total']
            had_coin.fee = float(had_coin.fee) + \
                orderSum['fee']

            had_coin.status = 0
            had_coin.transaction_time = datetime.datetime.now()
            had_coin.trailingstop_flag = 0
            had_coin.max = had_coin.price

            db.delete(order)

            transactionLog = models.possessionLog()
            transactionLog.coin = order.coin
            transactionLog.unit = orderSum['unit']
            transactionLog.price = orderStatus['data']['contract'][0]['price']
            transactionLog.total = orderSum['total']
            transactionLog.fee = orderSum['fee']
            transactionLog.status = 0
            transactionLog.transaction_time = order.transaction_time
            transactionLog.conclusion_time = datetime.datetime.now()
            transactionLog.type = 'bid'
            transactionLog.order_id = order.order_id
            db.add(transactionLog)

        if orderStatus['data']['order_status'] == 'Pending':
            orderSum = {'unit': 0, 'total': 0, 'fee': 0}
            if len(orderStatus['data']['contract']) > 0:
                for cont in orderStatus['data']['contract']:
                    orderSum['unit'] += cont['units']
                    orderSum['total'] += cont['total']
                    orderSum['fee'] += cont['fee']

                orderSum['price'] = orderStatus['data']['order_price']

                trading = db.query(models.possessionCoin).filter(
                    models.possessionCoin.coin == orderStatus['data']['order_currency'])

                trading.unit = orderSum['unit']
                trading.total = orderSum['total']
                trading.price = orderSum['price']
                trading.fee = orderSum['fee']

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

    # 매도 확인
    if order.status == 3 or order.status == 5:
        isOrder = []

        order_desc = ['ask', order.coin, order.order_id, 'KRW']
        orderStatus = bithumb.get_order_completed(order_desc)
        Possession = db.query(models.possessionCoin).filter(
            models.possessionCoin.coin == order.coin).first()

        if orderStatus['data']['order_status'] == 'Completed':
            orderSum = {'unit': 0, 'total': 0, 'fee': 0}

            for cont in orderStatus['data']['contract']:
                orderSum['unit'] += float(cont['units'])
                orderSum['total'] += float(cont['total'])
                orderSum['fee'] += float(cont['fee'])
            orderSum['price'] = orderStatus['data']['order_price']

            poseesionCheck = db.query(models.orderCoin).filter(
                models.orderCoin.coin == order.coin).all()
            db.delete(Possession)
            db.delete(order)

            for cont in orderStatus['data']['contract']:
                print(
                    'asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd')

            transactionLog = models.possessionLog()
            transactionLog.coin = order.coin
            transactionLog.unit = orderSum['unit']
            transactionLog.price = orderSum['price']
            transactionLog.total = orderSum['total']
            transactionLog.fee = orderSum['fee']
            transactionLog.status = 6
            transactionLog.transaction_time = order.transaction_time
            transactionLog.conclusion_time = datetime.datetime.now()
            transactionLog.type = 'ask'
            transactionLog.order_id = order.order_id
            transactionLog.sell_reason = order.sell_reason
            db.add(transactionLog)

        if orderStatus['data']['order_status'] == 'Pending':
            orderSum = {'unit': 0, 'total': 0, 'fee': 0}
            if len(orderStatus['data']['contract']) > 0:
                for cont in orderStatus['data']['contract']:
                    orderSum['unit'] += cont['units']
                    orderSum['total'] += cont['total']
                    orderSum['fee'] += cont['fee']

                orderSum['price'] = orderStatus['data']['order_price']

                trading = db.query(models.possessionCoin).filter(
                    models.possessionCoin.coin == orderStatus['data']['order_currency'])

                trading.unit = trading.unit - orderSum['unit']
                trading.total = trading.total - orderSum['total']
                trading.price = orderSum['price']
                trading.fee = trading.fee - orderSum['fee']

                db.commit()

            timeCheck = str(datetime.datetime.strptime(
                order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
            print(timeCheck[0])

            if timeCheck[0] == '-':
                if len(orderStatus['data']['contract']) > 0:
                    if trading.total < 1000:
                        continue

                cancel = bithumb.cancel_order(order_desc)
                if cancel == True:
                    db.delete(order)
                    Possession.status = 4

        print(orderStatus)
        db.commit()

print('process end')
