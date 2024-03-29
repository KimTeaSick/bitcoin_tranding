from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pybithumb import Bithumb
from sqlalchemy import and_
import threading
import datetime
import models

def orderCheck(user, db):
    try:
        bithumb = Bithumb(user.public_key, user.secret_key)
        krTime = 60 * 60 * 9
        # 주문 확인 매매 성공 확인, 취소
        orderList = db.query(models.orderCoin).filter(
                models.orderCoin.user_idx == user.idx).all()
        possession_list = db.query(models.possessionCoin).filter(
                models.possessionCoin.user_idx == user.idx).all()
        for order in orderList:
            print("buy order status order_id ::: ::: ", order.order_id)
            # 매수 확인
            if order.status == 1:
                order_desc = ['bid', order.coin, order.order_id, 'KRW']
                orderStatus = bithumb.get_order_completed(order_desc)
                # BUY_CHECK(orderStatus, order, bithumb, db)
                print("buy order status ::: ::: ", user.idx, orderStatus)
                print("--------------------------------------------------------------------------")
                if orderStatus['data']['order_status'] == 'Completed':
                    had_coin = db.query(models.possessionCoin).filter(and_(
                        models.possessionCoin.coin == order.coin, 
                        models.possessionCoin.user_idx == user.idx)).first()
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
                        trading = db.query(models.possessionCoin).filter(and_(
                            models.possessionCoin.coin == orderStatus['data']['order_currency'],
                            models.possessionCoin.user_idx == user.idx))
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
                        delpossession = db.query(models.possessionCoin).filter(and_(
                            models.possessionCoin.coin == order.coin,
                            models.possessionCoin.user_idx == user.idx)).first()
                        # 분할매도에 완전히 실패할 경우 내역에서 제거하는 로직
                        cancel = bithumb.cancel_order(order_desc)
                        if cancel == True:
                            db.delete(order)
                            if len(orderStatus['data']['contract']) != 0:
                                db.delete(delpossession)
                if orderStatus['data']['order_status'] == 'Cancel':
                    db.delete(order)
                print(orderStatus)
                db.commit()
            # 매도 확인
            if order.status == 3 or order.status == 5:
                order_desc = ['ask', order.coin, order.order_id, 'KRW']
                print("order_desc ::: ::: ", order_desc)
                orderStatus = bithumb.get_order_completed(order_desc)
                print("orderStatus ::: ::: ", orderStatus)
                if orderStatus == None : continue
                print("---------------------------------------------------------------------------------")
                if orderStatus['data']['order_status'] == 'Completed':
                    Possession = db.query(models.possessionCoin).filter(and_(
                        models.possessionCoin.user_idx == order.user_idx,
                        models.possessionCoin.coin == order.coin)).first()
                    if Possession == None : 
                        db.delete(order)
                        continue
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
                    print("delete Possession ::: ::: ", user.idx, Possession.coin)
                    for cont in orderStatus['data']['contract']:
                        print('contract', cont)
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
                        trading = db.query(models.possessionCoin).filter(and_(
                            models.possessionCoin.coin == orderStatus['data']['order_currency'],
                            models.possessionCoin.user_idx == user.idx,)).first()
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
                if orderStatus['data']['order_status'] == 'Cancel':
                    Possession = db.query(models.possessionCoin).filter(and_(
                        models.possessionCoin.user_idx == order.user_idx,
                        models.possessionCoin.coin == order.coin
                        )).first()
                    print('Cancel')
                    db.delete(order)
                    Possession.status = 4
                print(orderStatus)
                db.commit()
        for p_coin in possession_list:
            if p_coin.status == 1:
                order_desc = ['bid', p_coin.coin, p_coin.order_id, 'KRW']
                coin_order_status = bithumb.get_order_completed(order_desc)
                if coin_order_status['data']['order_status'] == 'Cancel':
                    d_order = db.query(models.orderCoin).filter(and_(
                        models.orderCoin.user_idx == user.idx,
                        models.orderCoin.coin == p_coin.coin)).first()
                    db.delete(p_coin)
                    db.delete(d_order)
                    db.commit()
                if coin_order_status['data']['order_status'] == 'Completed':
                    print("com_coin ::: ::: ", p_coin.coin)
                    order_sum = {'unit': 0, 'total': 0, 'fee': 0}
                    for cont in coin_order_status['data']['contract']:
                        order_sum['unit'] += float(cont['units'])
                        order_sum['total'] += float(cont['total'])
                        order_sum['fee'] += float(cont['fee'])
                    p_coin.unit = float(p_coin.unit) + order_sum['unit']
                    print("p_coin.unit", p_coin.unit)
                    p_coin.price = float(p_coin.price) + float(coin_order_status['data']['order_price'])
                    p_coin.total = float(p_coin.total) + order_sum['total']
                    p_coin.fee = float(p_coin.fee) + order_sum['fee']
                    p_coin.status = 0
                    p_coin.transaction_time = datetime.datetime.now()
                    p_coin.trailingstop_flag = 0
                    p_coin.max = p_coin.price
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
                        print("pen_coin ::: ::: ", p_coin.coin)
                        p_coin.unit = order_sum['unit']
                        p_coin.total = order_sum['total']
                        p_coin.price = order_sum['price']
                        p_coin.fee = order_sum['fee']
                        db.commit()
        print('process end')
    except Exception as e:
        print("orderCheck Error ::::: ",e)
        db.rollback()
    finally:
        print("user idx ", user.idx, " end")
        db.close()


if __name__ == "__main__":
    now1 = datetime.datetime.now()
    try:
        db = SessionLocal()
        db: Session
        bithumbUsers = db.query(models.USER_T).filter(models.USER_T.platform == '1').all()
        for user in bithumbUsers:
            forInDb = SessionLocal()
            forInDb: Session
            t = threading.Thread(target=orderCheck, args=[user, forInDb])
            t.start()
    finally:
        print("process end !!!")
        db.close()