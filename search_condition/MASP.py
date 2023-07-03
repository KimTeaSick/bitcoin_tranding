import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np
from datetime import datetime 

bit = BitThumbPrivate()

def MASP_condition(coin_list):
    print("MASP_condition coin_list :::::", coin_list)
    first_period=15 
    second_period=60 
    return_value = []
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
      first_ema = close_price.ewm(span=first_period, adjust=False).mean()
      # 장기 지수 이동 평균 계산
      second_ema = close_price.ewm(span=second_period, adjust=False).mean()
      masp_data = pd.DataFrame({
        'Name': str(coin).replace("_KRW", ""),
        'First': first_ema,
        'Second': second_ema,
      })
      if float(masp_data.iloc[-1]['First']) > float(masp_data.iloc[-1]['Second']): 
          return_value.append(str(coin).replace("_KRW", ""))
          print("masp_data :::: ",masp_data.iloc[-1]['Name'])
    return return_value