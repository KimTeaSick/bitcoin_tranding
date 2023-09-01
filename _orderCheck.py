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

def orderCheck(idx):
    try:
        user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
        bit = Bithumb(user.public_key, user.secret_key)
        order_list = db.query(models.orderCoin).filter(models.orderCoin.user_idx == idx).all()
        for order in order_list:
            if order.status == 1:
                order_desc = ['bid', order.coin, order.order_id, 'KRW']
                orderStatus = bit.get_order_completed(order_desc)
                if orderStatus['data']['order_status'] == 'Completed':
                    order_info = {}
                    trading_log = models.possessionLog()
                    trading_log.coin = order.coin
                if orderStatus['data']['order_status'] == 'Pending':
                    print()

    except Exception as e:
        print("order Check Error ::: :::", e)
        db.rollback()
