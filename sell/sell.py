from sqlalchemy.orm import Session
from pybithumb import Bithumb
import threading
import datetime
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
from database import SessionLocal
from lib.getRate import now_rate_fn
import models
import askingPrice

def sell(active_user, db, models):
  try:
    bithumb = Bithumb(active_user.public_key, active_user.secret_key)
    sell_list = []
    possession_coins, useTradingOption, accountOtion, sellOption = sell_data.get_sell_condition(active_user, db, models)
    possession, nowWallet, isSell, resale, under_one_dollar = sell_cal.get_sell_list_cal(possession_coins)
    max_chart_time = sell_cal.get_max_chart_term_time(possession_coins, sellOption)
    # rate_percent = sell_data.get_rate_percent(nowWallet, possession)
    rate_percent = now_rate_fn(db, models, bithumb, active_user.idx)
    print("rate_percent", active_user.idx, rate_percent)
    sell_list.extend(sell_cal.re_sale_list_cal(resale, sellOption))
    sell_list.extend(sell_cal.loss_cut_under_list_cal(isSell, rate_percent, accountOtion))
    sell_list.extend(sell_cal.drop_down_coin_list_cal(isSell, sellOption))
    transaction_time = datetime.datetime.now()
    cancel_time = transaction_time + datetime.timedelta(seconds=accountOtion.buy_cancle_time)
    for sell_coin in sell_list:
      try:
        print("sell_coin", active_user.idx, sell_coin)
        if sell_coin['reason'] == "resale":
          order_id = sell_action.re_sell_coin_action(bithumb, sell_coin)
          print("resale order_id", order_id)
          order_info = sell_format.insert_order_format(models, sell_coin, order_id, transaction_time, cancel_time, active_user.idx, "resale")
          print("resale order_info", order_info) 
        else:
          ask = f'+{sellOption.call_money_to_sell_method}' if int(sellOption.call_money_to_sell_method) >= 0 else str(sellOption.call_money_to_sell_method)
          ask_price = askingPrice.ASK_PRICE(f"{sell_coin['coin']}", ask, 'sell')
          order_id = sell_action.sell_coin_action(bithumb, sell_coin, ask_price)
          print("other reason sell order_info", order_id)
          order_info = sell_format.insert_order_format(models, sell_coin, order_id, transaction_time, cancel_time, active_user.idx, "other")
          print("other reason sell order_info", order_info)
        db.add(order_info)
      except Exception as e:
        print(e)
        continue
    db.commit()
    print("sell complete", active_user.idx, ":::", sell_list)
  except Exception as error:
    print("Error ::: ", error)
    db.rollback()
  finally:
    db.close()


def sell_t(models):
  db = SessionLocal()
  db: Session
  active_users = sell_data.get_active_user(db, models)
  for active_user in active_users:
    db = SessionLocal()
    db : Session
    t = threading.Thread(target=sell, args=([active_user, db, models]))
    t.start()

sell_t(models)