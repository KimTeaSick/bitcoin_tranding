import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np

bit = BitThumbPrivate()

def MACD_condition():
    item = {"id": "CAKE", "term":"1h" }
    close_data = []
    date_data = []
    short_period=15 
    long_period=60 
    signal_period=9
    row_candle_data = bit.calndel_for_search(item)
    candle_data = list(row_candle_data.values())
    for data in candle_data[1]:
      close_data.append(float(data[2]))
      date_data.append(float(data[0]))
        # 단기 지수 이동 평균 계산
    data = pd.DataFrame({'date':date_data,'close':close_data})
    close_price = data['close']
    # print("close_data :::: ", close_price)
    short_ema = close_price.ewm(span=short_period, adjust=False).mean()
    # 장기 지수 이동 평균 계산
    long_ema = close_price.ewm(span=long_period, adjust=False).mean()
    # MACD 계산
    macd_line = short_ema - long_ema
    # MACD 신호선 계산
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    # MACD 히스토그램 계산
    histogram = macd_line - signal_line
    # 결과 데이터프레임 생성
    macd_data = pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    })
    print("macd_data :::: ",macd_data)
    return macd_data

MACD_condition()