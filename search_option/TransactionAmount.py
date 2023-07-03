import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np

bit = BitThumbPrivate()

def Transaction_amount_coondtion(coin_list, low_limit, high_limit):
  return_value =[]
  for coin in coin_list:
    item = {"id": str(coin[0]).replace("_KRW", ""), "term": "1h"}
    # row_candle_data = bit.calndel_for_search(item)
    row_data = bit.getBitCoinList(item['id'])
    data = row_data['data']
    print("row_candle_data :::: ", data)
    if float(data['acc_trade_value_24H']) > float(low_limit) and float(data['acc_trade_value_24H']) <= float(high_limit): pass
    else: 
      return_value.append(str(coin[0]).replace("_KRW", ""))
  #   candle_data = list(row_candle_data.values())
  #   if float(candle_data[1][-1][2]) * float(candle_data[1][-1][5]) > float(low_limit) and float(candle_data[1][-1][2]) * float(candle_data[1][-1][5]) <= float(high_limit): pass
  #   else: 
  #     return_value.append(str(coin[0]).replace("_KRW", ""))
  print("Transaction_amount_coondtion return_value :::: ", return_value)
  return return_value