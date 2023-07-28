from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from BitThumbPrivate import BitThumbPrivate

class TestFn():
  def __init__(self):
    self.bithumb = BitThumbPrivate()

  def signTradeFn(self, order):
    order_desc= [order.type, order.coin, order.order_id, 'KRW']
    orderStatus = self.bithumb.bithumb.get_order_completed(order_desc)
    return orderStatus
  
  def cancleTradeFn(self, order):
    order_desc= [order.type, order.coin, order.order_id, 'KRW']
    orderStatus = self.bithumb.bithumb.cancel_order(order_desc)
    return orderStatus