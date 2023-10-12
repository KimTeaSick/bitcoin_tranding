from sqlalchemy.orm import Session

import threading

import sell_data
import sell_cal
import sell_action
import sell_format

import os
from dotenv import load_dotenv
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
DEV_PWD = os.environ.get('DEV_PWD')
PRO_PWD = os.environ.get('PRO_PWD')
pwd = DEV_PWD if IS_DEV == "True" else PRO_PWD
import sys 
sys.path.append(pwd) 
from database import engine, SessionLocal

def sell(active_user, db):
  sell_list = []
  possession_coins, useTradingOption, accountOtion, sellOption = sell_data.get_sell_condition(active_user, db)
  possession, nowWallet, isSell, resale, under_one_dollar = sell_cal.get_sell_list_cal(possession_coins)
  max_chart_time = sell_cal.get_max_chart_term_time(possession_coins, sellOption)
  rate_percent = sell_data.get_rate_percent(nowWallet, possession)
  sell_list.extend(sell_cal.re_sale_list_cal(resale, sellOption))
  sell_list.extend(sell_cal.loss_cut_under_list_cal(isSell, rate_percent, accountOtion))
  sell_list.extend(sell_cal.drop_down_coin_list_cal(isSell, sellOption))
  print(active_user.idx, sell_list)

def sell_t():
  db = SessionLocal()
  db: Session
  active_users = sell_data.get_active_user(db)
  print("active_users", active_users)
  for active_user in active_users:
    db = SessionLocal()
    db : Session
    t = threading.Thread(target=sell, args=([active_user, db]))
    t.start()

sell_t()