from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from pybithumb import Bithumb

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

active_users = db.query(models.USER_T).all()

for user in active_users:
  try:
    bithumb = Bithumb(user.public_key, user.secret_key)
    krTime = 60 * 60 * 9
    # 주문 확인 매매 성공 확인, 취소
    orderList = db.query(models.orderCoin).filter(
            models.orderCoin.user_idx == user.idx).all()
    possession_list = db.query(models.possessionCoin).filter(
            models.possessionCoin.user_idx == user.idx).all()

    for p_coin in possession_list:
        if p_coin.status == 1:
            order_desc = ['bid', p_coin.coin, p_coin.order_id, 'KRW']
            coin_order_status = bithumb.get_order_completed(order_desc)
            if coin_order_status['data']['order_status'] == 'Cancel':
                db.delete(p_coin)
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
    
  except Exception as e:
    print(e)