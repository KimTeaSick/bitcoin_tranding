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

bit = BitThumbPrivate()

def Trend_condition(coin_list, masp, t_trend_term, up_down):
    trend_term = 15
    return_coin = []
    close_data =[]
    date_data =[]
    for coin in coin_list:
      item = {"id": str(coin).replace("_KRW", ""), "term": "1h"}
      trend_result = []
      row_candle_data = bit.calndel_for_search(item)
      candle_data = list(row_candle_data.values())
      for data in candle_data[1]:
        close_data.append(float(data[2]))
        date_data.append(float(data[0]))
      pd_data = pd.DataFrame({'date':date_data,'close':close_data})
      close_price = pd_data['close']
      masp_ema = close_price.ewm(span=int(masp), adjust=False).mean()
      trend_data = pd.DataFrame({
        'Name':  str(coin).replace("_KRW", ""),
        'masp': masp_ema,
      })
      arr_data = list(trend_data['masp'].iloc[-(int(t_trend_term) + 1):])

      for i in range(int(t_trend_term)):
        diff = arr_data[i] - arr_data[i + 1]
        trend_result.append(diff)

      if up_down == 'up_trend': # 상승 추세
        flag = False
        for element in trend_result:
          if element < 0:
              flag = True
          else: 
            flag = False
            break
        if flag: 
          # print("trend :::: ", str(coin).replace("_KRW", ""))
          return_coin.append(str(coin).replace("_KRW", ""))
      
      if up_down == 'down_trend': # 하락 추세
        flag = False
        for element in trend_result:
          if element > 0:
              flag = True
          else: 
            flag = False 
            break
        if flag: 
          # print("trend :::: ", str(coin).replace("_KRW", ""))
          return_coin.append(str(coin).replace("_KRW", ""))

    print("trend_condition return_coin :::: ", return_coin)
    return return_coin