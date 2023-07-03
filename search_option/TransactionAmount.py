import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 
from BitThumbPrivate import BitThumbPrivate
import pandas as pd
import numpy as np

bit = BitThumbPrivate()

def Transaction_amount_coondtion(coin_list, low_limit, high_limit):
  print("coin_list :::: ", coin_list)
  return_value =[]
  for coin in coin_list:
    item = {"id": str(coin).replace("_KRW", ""), "term": "1h"}
    row_data = bit.getBitCoinList(item['id'])
    data = row_data['data']
    if float(data['acc_trade_value_24H']) > float(low_limit) and float(data['acc_trade_value_24H']) <= float(high_limit): pass
    else: 
      return_value.append(str(coin).replace("_KRW", ""))
  print("Transaction_amount_coondtion return_value :::: ", return_value)
  return return_value