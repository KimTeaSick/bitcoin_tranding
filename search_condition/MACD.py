import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np

bit = BitThumbPrivate()

def MACD_condition(coin_list, chart_term, short, long, signal,):
    print("MACD_condition coin_list :::::", coin_list)
    close_data = []
    date_data = []
    return_value =[]
    for coin in coin_list:
        item = {"id": str(coin).replace("_KRW", ""), "term": chart_term}
        row_candle_data = bit.calndel_for_search(item)
        candle_data = list(row_candle_data.values())
        print("MACD_condition candle_data :::::", candle_data)
        for data in candle_data[1]:
            print("MACD_condition data :::::", data)
            close_data.append(float(data[2]))
            date_data.append(float(data[0]))
        pd_data = pd.DataFrame({'date':date_data,'close':close_data})
        close_price = pd_data['close']
        # print("close_data :::: ", close_price)
        short_ema = close_price.ewm(span=short, adjust=False).mean()
        # 장기 지수 이동 평균 계산
        long_ema = close_price.ewm(span=long, adjust=False).mean()
        # MACD 계산
        macd_line = short_ema - long_ema
        # MACD 신호선 계산
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        # MACD 히스토그램 계산
        histogram = macd_line - signal_line
        # 결과 데이터프레임 생성
        macd_data = pd.DataFrame({
            # 'Name': coin_name,
            'Name': str(coin).replace("_KRW", ""),
            'MACD': macd_line,
            'Signal': signal_line,
            'Histogram': histogram
        })
        if float(macd_data.iloc[-1]['Signal']) > float(macd_data.iloc[-1]['MACD']): 
            return_value.append(str(coin).replace("_KRW", ""))
            print("macd_data :::: ",macd_data.iloc[-1]['Name'])
    
    return return_value
