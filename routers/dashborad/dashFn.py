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
from .dashLib import DASH_LIB
from platformPrivate import BitThumbPrivate
from chartMaker import ChartMaker
import datetime 
import models
import time

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

lib = DASH_LIB()

class DashBoardFn():
  async def rateCheck(self, item, bit, idx):
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
      db.rollback()
      print('rate_check Error ::: ::: ', e)
  
  async def all_user_deposit_fn(self):
    try:
      users = db.query(models.USER_T).all()
      total = 0
      for user in users:
        if user.idx == 13: 
          continue
        balance = lib.sum_all_user_money(user.idx)
        total += balance
      return total
    except Exception as e:
      db.rollback()
      print('all_user_deposit_fn Error ::: ::: ', e)

  # async def possessoionCoinInfo(self, idx, bit):
  #   try:
  #     possessionCoin = await bit.mysql.Select(getMyCoinListSql(idx))
  #     if len(possessionCoin) == 0:
  #       return 203
  #     else:
  #       returnList = []
  #       for coin in possessionCoin:
  #         print("coin :::", coin)
  #         coinInfo = bit.getBitCoinList(coin[1])['data']
  #         coinValue = float(coinInfo['closing_price'])
  #         returnList.append(
  #           changer.POSSESSION_COIN_LIST(coin, coinValue))
  #       return returnList
  #   except Exception as e:
  #     print("possessoionCoinInfo Error :::: ", e)
  #     db.rollback()
  #     return 333
    
  async def dashProperty(self, date, bit):
    coinList = bit.getMyCoinList()
    time.sleep(1)
    dt = datetime.now().replace()
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
    
  async def getUsersRateInfoFn(self,idx, bit):
    try:
      user_name = await bit.mysql.Select(users_info_sql(idx))
      user_total = await bit.mysql.Select(users_total_acc_sql(idx))
      data = await lib.getDashboardUserRateDataLib(bit, idx)
      return {
        "date_info": {
          "name": user_name[0][0],
          "total": user_total,
          "table_data": data
          }
        }
    except Exception as e :
       print("get_users_rate_info Error ::: :::", e) 
    
  async def day_week_month_data_fn(self, idx, bit):
    try:
      criteria_date = datetime.datetime.now() - datetime.timedelta(days=28)
      print("date ::: ::: ", criteria_date)
      data = await lib.get_day_week_month_data(bit, idx)
      return {"day_data": {"table_data": data[0],"his_data": data[3]}, 
              "week_data": {"table_data": data[1], "his_data": data[4]}, 
              "month_data": {"table_data": data[2], "his_data": data[5]} }
    except:
      db.rollback()
      raise

  async def getCurrentRateFn(self, idx):
    try:
      user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
      bit = BitThumbPrivate(user.public_key, user.secret_key)
      rate = await bit.nowRateFn(idx)
      print("rate ::::::: ", rate)
      return rate
    except Exception as e:
      print("getCurrentRateFn Error", e)
      db.rollback()

  async def getTotalOperateMoney(self, bit):
    try:
      now = datetime.datetime.now()
      rawTime = str(now.time())
      time = rawTime[0: 2]
      date = str(now.date()).replace("-","") + str(time) + "0000"
      res = await bit.mysql.Select(getTotalOperateMoneySql(date))
      print("TotalOperateMoney",res)
      return res[0][0]
    except Exception as e:
      print("Error ",e)

  async def getChartDataFn(self, idx, term):
    try:
      chartMaker = ChartMaker()
      returnValue = await chartMaker.getChartData(idx, term)
      print("getChartDataFn idx, term", returnValue)
      # rawDateData = await bit.mysql.oneSelect(getDateDataSql(idx))
      # rawChartData = await bit.mysql.oneSelect(getChartDataSql(idx))
      # return rawDateData, rawChartData
      return returnValue
    except Exception as e:
      print(e)

  async def getUserCountFn(self, bit, now):
    page = {}
    userCount = await bit.mysql.oneSelect(getUserCountSql)
    page["now"] = now
    page["count"] = int(round(userCount[0] / 4, 0))
    page["next"] = now + 1 if now != page["count"] else page["count"]
    page["prev"] = now - 1 if now != 1 else 1
    return page
  
  async def getUserListFn(self, bit, now):
    userList = await bit.mysql.oneSelect(getTableUserList(now))
    print("userList", userList)
    return userList