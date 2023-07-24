from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from BitThumbPrivate import BitThumbPrivate
from dbConnection import *
from sqld import *
import pandas as pd
import numpy as np
from datetime import datetime 
from .search_pipe import search_pipe, raw_search_pipe
from .pipe import Price_value_pipe
from .MACD import MACD_condition
from .MASP import MASP_condition
from .Trend import Trend_condition
from .Disparity import Disparity_condition
from .TransactionAmount import Transaction_amount_coondtion


bit = BitThumbPrivate()
mysql = MySql()

async def raw_search(item):
  start = datetime.now()
  return_value =[]
  condition = raw_search_pipe(item)
  result = []
  if condition['p_flag'] == '1': 
    raw_data = await mysql.Select(get_coin_close_price(condition['p_low_price'], condition['p_high_price'])) # 가격
    result = Price_value_pipe(raw_data)
    price= result[1]
    result = result[0]
  if condition['ta_flag'] == '1': result = Transaction_amount_coondtion(result, condition['ta_low_transaction_amount'], condition['ta_high_transaction_amount']) # 거래 대금
  if condition['masp_flag'] == '1': result = MASP_condition(result,condition['masp_first_disparity'],condition['masp_comparison'], condition['masp_second_disparity']) # MASP 비교
  if condition['t_flag'] == '1': result = Trend_condition(result, condition['t_MASP'],condition['t_trend_term'], condition['t_trend_type'])
  if condition['d_flag'] == '1': 
    result = Disparity_condition(result, condition['d_disparity_term'],condition['d_low_disparity'], condition['d_high_disparity']) # 이격도 비교
    disparity = result[1]
    result = result[0]
  if condition['macd_flag'] == '1': result = MACD_condition(result, condition['macd_chart_term'], condition['macd_short_disparity'], condition['macd_long_disparity'], condition['macd_signal'], condition['macd_up_down']) # MACD 비교

  for coin in result:
    row_data = bit.getBitCoinList(coin)
    data = row_data['data']
    return_value.append({coin:{'disparity': disparity[0][coin]['disparity'], 'close':price[0][coin]['Close']}})

  end = datetime.now()
  print("time :::: ", end - start)
  return return_value

async def search():
  start = datetime.now()
  search_option = await mysql.Select(get_search_option)
  condition = search_pipe(search_option[0])
  print("condition :::: ", condition)
  result = []
  return_value = []
  if condition['p_flag'] == '1':
    raw_data = await mysql.Select(get_coin_close_price(condition['p_low_price'], condition['p_high_price'])) # 가격
    result = Price_value_pipe(raw_data)
    price= result[1]
    result = result[0]
  if condition['ta_flag'] == '1': result = Transaction_amount_coondtion(result, condition['ta_low_transaction_amount'], condition['ta_high_transaction_amount']) # 거래 대금
  if condition['masp_flag'] == '1': result = MASP_condition(result,condition['masp_first_disparity'],condition['masp_comparison'], condition['masp_second_disparity']) # MASP 비교
  if condition['t_flag'] == '1': result = Trend_condition(result, condition['t_MASP'],condition['t_trend_term'], condition['t_trend_type'])
  if condition['d_flag'] == '1': 
    result = Disparity_condition(result, condition['d_disparity_term'],condition['d_low_disparity'], condition['d_high_disparity']) # 이격도 비교
    disparity = result[1]
    result = result[0]
  if condition['macd_flag'] == '1': result = MACD_condition(result, condition['macd_chart_term'], condition['macd_short_disparity'], condition['macd_long_disparity'], condition['macd_signal'], condition['macd_up_down']) # MACD 비교
  
  for coin in result:
    row_data = bit.getBitCoinList(coin)
    data = row_data['data']
    return_value.append({coin:{'disparity': disparity[0][coin]['disparity'], 'close':price[0][coin]['Close']}})
  end = datetime.now()
  print("time :::: ", end - start)
  return result

# asyncio.run(search())