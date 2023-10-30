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
from BitThumbPrivate import BitThumbPrivate
import datetime 
import models
import time

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class DASH_LIB():

  def sum_all_user_money(self, idx):
    try:
      user_info = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
      bit = BitThumbPrivate(user_info.public_key, user_info.secret_key)
      money = bit.myProperty()
      return int(money[0])
    except Exception as e:
      db.rollback()
      print("sum_all_user_money Error ::: ::: ", e )
  
  async def get_day_avg_cal(self, bit, idx):
    day_table_data = []
    for index in range(7):
      try:
        day_start_acc = await bit.mysql.Select(day_start_acc_sql(idx, index))
        day_end_acc = await bit.mysql.Select(day_end_acc_sql(idx, index))
        print(day_start_acc, day_end_acc)
        day_rate = round((day_end_acc[0][0] / day_start_acc[0][0]) * 100 - 100, 4)
        day_revenue = day_end_acc[0][0] - day_start_acc[0][0]
        # day_data = await bit.mysql.Select(day_avg_data_sql(idx, index))
        day_data = []
        # day_data = list(day_data[0])
        day_data.append(day_revenue)
        day_data.append(day_rate)
        day_table_data.append(day_data)
      except:
        day_table_data.append([0, 0])
        continue
    return day_table_data

  async def get_week_avg_cal(self, bit, idx):
    week_table_data = []
    for index in range(4):
      try:
        week_start_acc = await bit.mysql.Select(week_start_acc_sql(idx, index))
        week_end_acc = await bit.mysql.Select(week_end_acc_sql(idx, index))
        week_rate = round((week_end_acc[0][0] / week_start_acc[0][0]) * 100 - 100, 4)
        week_revenue = week_end_acc[0][0] - week_start_acc[0][0]
        # week_data = await bit.mysql.Select(week_avg_data_sql(idx, index))
        week_data = []
        # week_data = list(week_data[0])
        week_data.append(week_revenue)
        week_data.append(week_rate)
        week_table_data.append(week_data)
      except:
        week_table_data.append([0, 0])
        continue
    return week_table_data
  
  async def get_month_avg_cal(self, bit, idx):
    month_table_data = []
    for index in range(12):
      try:
        month_data = await bit.mysql.Select(month_avg_data_sql(idx, index))
        month_start_acc = await bit.mysql.Select(month_start_acc_sql(idx, index))
        month_end_acc = await bit.mysql.Select(month_end_acc_sql(idx, index))
        month_rate = round((month_end_acc[0][0] / month_start_acc[0][0]) * 100 - 100, 4)
        month_revenue = month_end_acc[0][0] - month_start_acc[0][0]
        # month_data = list(month_data[0])
        month_data = []
        month_data.append(month_revenue)
        month_data.append(month_rate)
        month_table_data.append(month_data)
      except:
        month_table_data.append([0, 0])
        continue
    return month_table_data

  async def get_day_week_month_data(self, bit, idx):
    day_table_data = await self.get_day_avg_cal(bit, idx)
    week_table_data = await self.get_week_avg_cal(bit, idx)
    month_table_data = await self.get_month_avg_cal(bit, idx)
    day_his_data =  await bit.mysql.Select(his_data_sql(idx, str(datetime.datetime.now() - datetime.timedelta(days=7))))
    week_his_data = await bit.mysql.Select(his_data_sql(idx, str(datetime.datetime.now() - datetime.timedelta(days=28))))
    month_his_data = await bit.mysql.Select(his_data_sql(idx, str(datetime.datetime.now() - datetime.timedelta(days=365))))
    return day_table_data, week_table_data, month_table_data, day_his_data, week_his_data, month_his_data
  
  async def get_dashboard_user_rate_data_lib(self, bit, idx):
    return_value = []
    standard_acc = await bit.mysql.Select(get_user_acc_info(idx, 0))
    day_acc = await bit.mysql.Select(get_user_acc_info(idx, 1))
    week_acc = await bit.mysql.Select(get_user_acc_info(idx, 7))
    month_acc = await bit.mysql.Select(get_user_acc_info(idx, 30))
    if len(day_acc) == 0:
      day_acc = await bit.mysql.Select(max_day_acc_info(idx))
    if len(week_acc) == 0:
      week_acc = await bit.mysql.Select(max_day_acc_info(idx))
    if len(month_acc) == 0:
      month_acc = await bit.mysql.Select(max_day_acc_info(idx))

    day_revenue = standard_acc[0][0] - day_acc[0][0]

    week_revenue = standard_acc[0][0] - week_acc[0][0]
    month_revenue = standard_acc[0][0] - month_acc[0][0]

    day_rate = standard_acc[0][0] / day_acc[0][0] * 100 - 100

    week_rate = standard_acc[0][0] / week_acc[0][0] * 100 - 100
    month_rate = standard_acc[0][0] / month_acc[0][0] * 100 - 100
    return_value.append([day_rate, day_revenue])
    return_value.append([week_rate, week_revenue])
    return_value.append([month_rate, month_revenue])
    return return_value
