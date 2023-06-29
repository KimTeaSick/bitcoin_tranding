import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np
from datetime import datetime 

bit = BitThumbPrivate()

def MASP_condition():
    start = datetime.now()
    row_bithumb_coin_list = bit.getBitCoinList('ALL')
    bithumb_coin_list = row_bithumb_coin_list['data'].keys()
    for coin in bithumb_coin_list:
      item = {"id": coin, "term": "1h"}
      row_candle_data = bit.calndel_for_search(item)
      print("bithumb_coin_list", row_candle_data)
    end = datetime.now()
    print("time :::: ", end - start)

MASP_condition()