from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from returnValue import changer
 
from sql.tradeHisSql import *
from routers.user.user_api import user

class TradeHisFn():
  def __init__(self):
    self.count = '14'

  async def orderListPageCount(self,idx, bit):
    value = await bit.mysql.Select(orderListCountSql(str(idx)))
    count = int(value[0][0]) / int(self.count)
    return round(count)

  async def getOrderList(self,idx, page, bit):
    prev = "0" if page == 1 else str((int(page) - 1) * 14)
    selectData = await bit.mysql.Select(orderListSql(str(idx), self.count, prev))
    orderList = []
    for data in selectData:
      orderList.append(changer.ORDER_LIST_CHANGER(data))
    return orderList
  
  def getDateOrderList(self, date, page, bit):
    prev = "0" if page == 1 else str((int(page) - 1) * 14)
    selectData = bit.mysql.Select(
      dateOrderListSql(self.count, prev, date[0], date[1]))
    orderList = []
    for data in selectData:
      orderDesc = (data[2], data[1], data[3], 'KRW')
      orderList.append(
        bit.bithumb.get_order_completed(orderDesc)['data'])
    return orderList