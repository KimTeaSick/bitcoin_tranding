import pandas as pd
from .getCandleInfo import getCandleInfo

def MASPCondition(coinList, option):
    return_coin = []
    close_data = []
    date_data = []
    for coin in coinList:
      item = {"id": coin['coin_name'], "term": option['chart_term']}
      row_candle_data = getCandleInfo(item)
      print("row_candle_data", row_candle_data)
      candle_data = list(row_candle_data.values())
      for data in candle_data[1]:
          close_data.append(float(data[2]))
          date_data.append(float(data[0]))
      pd_data = pd.DataFrame({'date':date_data,'close':close_data})
      close_price = pd_data['close']
      first_ema = close_price.ewm(span=int(option['first_disparity']), adjust=False).mean()
      second_ema = close_price.ewm(span=int(option['second_disparity']), adjust=False).mean()
      masp_data = pd.DataFrame({
        'Name': str(coin).replace("_KRW", ""),
        'First': first_ema,
        'Second': second_ema,
      })
      if option['comparison'] == '>=':
        if float(masp_data.iloc[-1]['First']) >= float(masp_data.iloc[-1]['Second']): 
          return_coin.append(coin)
      elif option['comparison'] == '<=':
        if float(masp_data.iloc[-1]['First']) <= float(masp_data.iloc[-1]['Second']): 
          return_coin.append(coin)
    print("masp_data return_coin :::: ", return_coin)
    return return_coin