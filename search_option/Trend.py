import pandas as pd
from .getCandleInfo import getCandleInfo

def TrendCondition(coin_list, option):
    return_coin = []
    close_data =[]
    date_data =[]
    for coin in coin_list:
      item = {"id": coin['coin_name'], "term": option['chart_term']}
      trend_result = []
      row_candle_data = getCandleInfo(item)
      candle_data = list(row_candle_data.values())
      for data in candle_data[1]:
        close_data.append(float(data[2]))
        date_data.append(float(data[0]))
      pd_data = pd.DataFrame({'date':date_data,'close':close_data})
      close_price = pd_data['close']
      masp_ema = close_price.ewm(span=int(option['MASP']), adjust=False).mean()
      trend_data = pd.DataFrame({
        'Name':  str(coin).replace("_KRW", ""),
        'masp': masp_ema,
      })
      arr_data = list(trend_data['masp'].iloc[-(int(option['trend_term']) + 1):])

      for i in range(int(option['trend_term'])):
        diff = arr_data[i] - arr_data[i + 1]
        trend_result.append(diff)

      if option['trend_type'] == 'up_trend': # 상승 추세
        flag = False
        for element in trend_result:
          if element < 0:
              flag = True
          else: 
            flag = False
            break
        if flag: 
          return_coin.append(coin)
      
      if option['trend_type'] == 'down_trend': # 하락 추세
        flag = False
        for element in trend_result:
          if element > 0:
              flag = True
          else: 
            flag = False 
            break
        if flag: 
          return_coin.append(coin)
    return return_coin