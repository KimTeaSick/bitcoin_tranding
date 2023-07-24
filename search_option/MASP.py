from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np
from datetime import datetime 

bit = BitThumbPrivate()

def MASP_condition(coin_list, first, comparison, second):
    return_coin = []
    close_data = []
    date_data = []
    for coin in coin_list:
      item = {"id": str(coin).replace("_KRW", ""), "term": "1h"}
      row_candle_data = bit.calndel_for_search(item)
      candle_data = list(row_candle_data.values())
      for data in candle_data[1]:
          close_data.append(float(data[2]))
          date_data.append(float(data[0]))
      pd_data = pd.DataFrame({'date':date_data,'close':close_data})
      close_price = pd_data['close']
      # print("close_data :::: ", close_price)
      first_ema = close_price.ewm(span=int(first), adjust=False).mean()
      # 장기 지수 이동 평균 계산
      second_ema = close_price.ewm(span=int(second), adjust=False).mean()
      masp_data = pd.DataFrame({
        'Name': str(coin).replace("_KRW", ""),
        'First': first_ema,
        'Second': second_ema,
      })
      if comparison == '>=':
        if float(masp_data.iloc[-1]['First']) >= float(masp_data.iloc[-1]['Second']): 
          return_coin.append(str(coin).replace("_KRW", ""))
      elif comparison == '<=':
        if float(masp_data.iloc[-1]['First']) <= float(masp_data.iloc[-1]['Second']): 
          return_coin.append(str(coin).replace("_KRW", ""))
    print("masp_data return_coin :::: ", return_coin)
    return return_coin