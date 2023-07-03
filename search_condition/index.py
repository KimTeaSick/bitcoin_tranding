import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
from dbConnection import *
from sql import *
import pandas as pd
import numpy as np
from search_pipe import *
from datetime import datetime 
from MACD import *
from MASP import *
from Trend import *
from Disparity import *
from TransactionAmount import *


bit = BitThumbPrivate()
mysql = MySql()

async def search():
  start = datetime.now()
  search_option = await mysql.Select(get_search_option)
  condition = search_pipe(search_option[0])
  print("condition :::: ", condition)
  result = []
  if condition['p_flag'] == '1': result = await mysql.Select(get_coin_close_price(condition['p_low_price'], condition['p_high_price'])) # 가격
  if condition['ta_flag'] == '1': result = Transaction_amount_coondtion(result, condition['ta_low_transaction_amount'], condition['ta_high_transaction_amount']) # 거래 대금
  if condition['macd_flag'] == '1': result = MACD_condition(result, condition['macd_chart_term'], condition['macd_short_disparity'], condition['macd_long_disparity'], condition['macd_signal']) # MACD 비교
  if condition['masp_flag'] == '1': result = MASP_condition(result) # MASP 비교
  if condition['d_flag'] == '1': result = Disparity_condition(result) # 이격도 비교
  end = datetime.now()
  print("result :::: ", result)
  print("time :::: ", end - start)
  return result

asyncio.run(search())