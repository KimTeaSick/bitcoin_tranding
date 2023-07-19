import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back")
from BitThumbPrivate import BitThumbPrivate
from returnValue import changer
from sql import *

class TradeHisFn():
  def __init__(self):
    self.bit = BitThumbPrivate()
    self.count = '14'

  async def orderListPageCount(self):
    value = await self.bit.mysql.Select(orderListCountSql)
    count = int(value[0][0]) / int(self.count)
    return round(count)

  async def getOrderList(self, page):
    prev = "0" if page == 1 else str((int(page) - 1) * 14)
    selectData = await self.bit.mysql.Select(orderListSql(self.count, prev))
    orderList = []
    for data in selectData:
      orderList.append(changer.ORDER_LIST_CHANGER(data))
    return orderList
  
  def getDateOrderList(self, date, page):
    prev = "0" if page == 1 else str((int(page) - 1) * 14)
    selectData = self.bit.mysql.Select(
      dateOrderListSql(self.count, prev, date[0], date[1]))
    orderList = []
    for data in selectData:
      orderDesc = (data[2], data[1], data[3], 'KRW')
      orderList.append(
        self.bit.bithumb.get_order_completed(orderDesc)['data'])
    return orderList