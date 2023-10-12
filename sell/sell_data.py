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
from sqlalchemy.orm import Session
import models
import datetime


now1 = datetime.datetime.now()


def get_active_user(db):
  try:
    return db.query(models.USER_T).filter(models.USER_T.active == 1).all()
  except:
    db.rollback()

def get_sell_condition(active_user, db):
  try:
    possession_coins = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == active_user.idx).all()
    useTradingOption = db.query(models.tradingOption).filter(models.tradingOption.idx == active_user.trading_option).first()
    accountOtion = db.query(models.tradingAccountOption).filter(models.tradingAccountOption.idx == useTradingOption.idx).first()
    sellOption = db.query(models.tradingSellOption).filter(models.tradingSellOption.idx == useTradingOption.idx).first()
    return possession_coins, useTradingOption, accountOtion, sellOption
  except:
    db.rollback()

def get_rate_percent(nowWallet, possession):
  try:
    percent = (nowWallet / possession) * 100 - 100
  except Exception as e:
    print(e)
    percent = 0
  return percent