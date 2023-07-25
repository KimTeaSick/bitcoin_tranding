from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 

from datetime import datetime 
from BitThumbPrivate import BitThumbPrivate
from returnValue import changer
from sql.dashBoardSql import *
import time

class DashBoardFn():
  def __init__(self):
    self.bit = BitThumbPrivate()

  async def rate_check(self, item):
    try:
      res = 0
      total_rate = await self.bit.mysql.Select(total_rate_sql(str(item.days)))
      for rate in total_rate:
        res += float(rate[0])
      print(total_rate[-1][-1])
      return round(res, 3), total_rate[-1][-1]
    except Exception as e:
      print('Error ::: ::: ', e)
  
  async def possessoionCoinInfo(self):
    try:
      possessionCoin = await self.bit.mysql.Select(getMyCoinListSql) #
      time.sleep(1)
      if len(possessionCoin) == 0:
        return 203
      else:
        returnList = []
        for coin in possessionCoin:
          coinInfo = self.bit.getBitCoinList(coin[0])['data']
          coinValue = float(coinInfo['closing_price'])
          returnList.append(
            changer.POSSESSION_COIN_LIST(coin, coinValue))
        # print("returnListreturnList", returnList)
        return returnList
    except Exception as e:
      print("possessoionCoinInfo Error :::: ", e)
      return 333
    
  async def dashProperty(self, date):
    coinList = self.bit.getMyCoinList()
    time.sleep(1)
    dt = datetime.now().replace()
    start_dt = dt[0:10] + "00:00:00.000000"
    end_dt = dt[0:10] + "23:59:59.999999"
    list = []
    fee = 0
    totalMoney = 0
    buyingMoney = 0
    sellingMoney = 0
    selectData = await self.bit.mysql.Select(todayOrderListSql(date[0], date[1])) #
    time.sleep(1)
    for i in coinList:
        coinInfo = self.bit.getBitCoinList(str(i[0]).replace('total_', ""))
        coinValue = float(
            coinInfo['data']['closing_price']) * round(float(i[1]), 4)
        list.append(coinValue)
    for index in range(len(list)):
        totalMoney += list[index]
    account = self.bit.checkAccount()
    totalMoney += account
    if selectData != 333:
        for todayData in selectData:
            if todayData[2] == 'ask':
                sellingMoney += float(todayData[9])
            else:
                buyingMoney += float(todayData[9])
            fee += float(todayData[8])
        accountData = [totalMoney, account, buyingMoney, sellingMoney, fee]
        return accountData