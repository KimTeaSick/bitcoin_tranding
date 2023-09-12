from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from sqlalchemy.orm import Session
from database import SessionLocal
from returnValue import changer
from sql.dashBoardSql import *
from datetime import datetime 
import models
import time

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class DashBoardFn():
  async def rate_check(self, item, bit, idx):
    try:
      res = 0
      print(str(item.days), str(int(item.days)+1))
      account_info = await bit.mysql.Select(total_rate_sql(str(item.days), idx))

      total_invest = await bit.mysql.Select(total_invest_sql(idx))
      total_withdraw = await bit.mysql.Select(total_withdraw_sql(idx))
      total_invest_money = int(total_invest[0][0] - total_withdraw[0][0])
      
      print("total_rate", account_info)
      return {"rate":round(res, 3), "account_balance": account_info[-1][1],
              "date": account_info[0][3][0:8] + " ~ " + account_info[-1][3][0:8],
              "table_data": account_info[::-1], "invest_money": total_invest_money}
    except Exception as e:
      print('rate_check Error ::: ::: ', e)
  
  async def possessoionCoinInfo(self, idx, bit):
    try:
      possessionCoin = await bit.mysql.Select(getMyCoinListSql(idx))
      if len(possessionCoin) == 0:
        return 203
      else:
        returnList = []
        for coin in possessionCoin:
          coinInfo = bit.getBitCoinList(coin[1])['data']
          coinValue = float(coinInfo['closing_price'])
          returnList.append(
            changer.POSSESSION_COIN_LIST(coin, coinValue))
        return returnList
    except Exception as e:
      print("possessoionCoinInfo Error :::: ", e)
      return 333
    
  async def dashProperty(self, date, bit):
    coinList = bit.getMyCoinList()
    time.sleep(1)
    dt = datetime.now().replace()
    start_dt = dt[0:10] + "00:00:00.000000"
    end_dt = dt[0:10] + "23:59:59.999999"
    list = []
    fee = 0
    totalMoney = 0
    buyingMoney = 0
    sellingMoney = 0
    selectData = await bit.mysql.Select(todayOrderListSql(date[0], date[1])) #
    time.sleep(1)
    for i in coinList:
        coinInfo = bit.getBitCoinList(str(i[0]).replace('total_', ""))
        coinValue = float(
            coinInfo['data']['closing_price']) * round(float(i[1]), 4)
        list.append(coinValue)
    for index in range(len(list)):
        totalMoney += list[index]
    account = bit.checkAccount()
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
    
  async def get_users_rate_info_Fn(self, bit):
    try:
      s_o = await bit.mysql.Select(get_users_rate_info_Sql(1, 1))
      o_o = await bit.mysql.Select(get_users_rate_info_Sql(8, 1))
      j_o = await bit.mysql.Select(get_users_rate_info_Sql(4, 1))
      s_s = await bit.mysql.Select(get_users_rate_info_Sql(1, 7))
      o_s = await bit.mysql.Select(get_users_rate_info_Sql(8, 7))
      j_s = await bit.mysql.Select(get_users_rate_info_Sql(4, 7))
      s_m = await bit.mysql.Select(get_users_rate_info_Sql(1, 30))
      o_m = await bit.mysql.Select(get_users_rate_info_Sql(8, 30))
      j_m = await bit.mysql.Select(get_users_rate_info_Sql(4, 30))
      arr = [s_o,o_o,j_o,s_s,o_s,j_s,s_m,o_m,j_m]
      for data in arr:
         if len(data) == 0:
            data.append(["-","-","-"])
            
      return {
        "shin_info": {
           "name": "신다해",
           "total": 550000,
           "table_data":[s_o[0], s_s[0], s_m[0]]
          }, 
        "oh_info": {
           "name": "오석표",
           "total": 8584623,
           "table_data":[o_o[0], o_s[0], o_m[0]]
          }, 
        "jo_info": {
           "name": "김요셉",
           "total": 500000,
           "table_data":[j_o[0], j_s[0], j_m[0]]
          }
        }
    except Exception as e :
       print("get_users_rate_info Error ::: :::", e) 
    