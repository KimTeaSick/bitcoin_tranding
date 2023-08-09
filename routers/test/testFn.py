from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from routers.user.userApi import user
 

class TestFn():
  def signTradeFn(self, order, bit):
    order_desc= [order.type, order.coin, order.order_id, 'KRW']
    orderStatus = bit.bithumb.get_order_completed(order_desc)
    return orderStatus
  
  def cancleTradeFn(self, order, bit):
    order_desc= [order.type, order.coin, order.order_id, 'KRW']
    orderStatus = bit.bithumb.cancel_order(order_desc)
    return orderStatus