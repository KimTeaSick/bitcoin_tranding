from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from pybithumb import Bithumb
from orderChecked.possessionExplore import possessionExplore
from orderChecked.buyCheck import BUY_CHECK

# 빗썸 api 키 오
# secretKey = "c59e7f376201984d26224428649e42c7"
# connenctKey = "e2fee448690937ae2e8cd6dada5a183e"

# 빗썸 api 키 신
# secretKey = "07c1879d34d18036405f1c4ae20d3023"
# connenctKey = "9ae8ae53e7e0939722284added991d55"


now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

# autoStatus = db.query(models.autoTradingStatus).filter(
#     models.autoTradingStatus.status == 1).first()

active_users = db.query(models.USER_T).all()

for user in active_users:
    bithumb = Bithumb(user.public_key, user.secret_key)

    if user.active == 0:
        print('자동 매매 정지 exit')
        exit()

    krTime = 60 * 60 * 9
    # 주문 확인 매매 성공 확인, 취소
    orderList = db.query(models.orderCoin).filter(
            models.orderCoin.user_idx == user.idx).all()
    for order in orderList:
        possession_list = db.query(models.possessionCoin).filter(
            models.possessionCoin.user_idx == user.idx).all()
        print("buy order status order_id ::: ::: ", order.order_id)
        # 매수 확인
        if order.status == 1:
            order_desc = ['bid', order.coin, order.order_id, 'KRW']
            orderStatus = bithumb.get_order_completed(order_desc)
            # BUY_CHECK(orderStatus, order, bithumb, db)
            print("buy order status ::: ::: ", orderStatus)
            print("--------------------------------------------------------------------------")

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

        # 매도 확인
        if order.status == 3 or order.status == 5:
            order_desc = ['ask', order.coin, order.order_id, 'KRW']
            print("order_desc ::: ::: ", order_desc)
            orderStatus = bithumb.get_order_completed(order_desc)
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

                poseesionCheck = db.query(models.orderCoin).filter(models.orderCoin.coin == order.coin).all()
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

                timeCheck = str(datetime.datetime.strptime(
                    order.cancel_time, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.now())
                print(timeCheck[0])
                if timeCheck[0] == '-':
                    if len(orderStatus['data']['contract']) > 0:
                        if float(trading.total) < 1000:
                            continue
                    cancel = bithumb.cancel_order(order_desc)
                    if cancel == True:
                        db.delete(order)
                        Possession.status = 4
            print(orderStatus)
            db.commit()
        possessionExplore(possession_list, bithumb, db)

    print('process end')
