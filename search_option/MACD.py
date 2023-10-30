from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
 
import pandas as pd
from .getCandleInfo import getCandleInfo

def MACDCondition(coin_list, option):
    # print("MACD_condition coin_list :::::", coin_list)
    close_data = []
    date_data = []
    return_coin =[]
    for coin in coin_list:
        item = {"id": coin['coin_name'], "term": option['chart_term']}
        row_candle_data = getCandleInfo(item)
        candle_data = list(row_candle_data.values())
        for data in candle_data[1]:
            close_data.append(float(data[2]))
            date_data.append(float(data[0]))
        pd_data = pd.DataFrame({'date':date_data,'close':close_data})
        close_price = pd_data['close']
        short_ema = close_price.ewm(span=int(option['short_disparity']), adjust=False).mean()
        long_ema = close_price.ewm(span=int(option['long_disparity']), adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=int(option['signal']), adjust=False).mean()
        histogram = macd_line - signal_line
        macd_data = pd.DataFrame({
            'Name': str(coin).replace("_KRW", ""),
            'MACD': macd_line,
            'Signal': signal_line,
            'Histogram': histogram
        })
        
        if option['up_down'] == 'up':
            if float(macd_data.iloc[-1]['Signal']) < float(macd_data.iloc[-1]['MACD']): 
                return_coin.append(str(coin).replace("_KRW", ""))
        elif option['up_down'] == 'down':
            if float(macd_data.iloc[-1]['Signal']) > float(macd_data.iloc[-1]['MACD']): 
                return_coin.append(str(coin).replace("_KRW", ""))

    print("macd_data return_coin :::: ", return_coin)
    return return_coin
