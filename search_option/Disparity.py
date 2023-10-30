import pandas as pd
from .getCandleInfo import getCandleInfo

def DisparityCondition(coin_list, option):
    return_coin=[]
    return_value=[{}]
    close_data =[]
    date_data =[]
    for coin in coin_list:
        item = {"id": coin['coin_name'], "term": option['chart_term']}
        row_candle_data = getCandleInfo(item)
        candle_data = list(row_candle_data.values())
        for data in candle_data[1]:
            close_data.append(float(data[2]))
            date_data.append(float(data[0]))
        pd_data = pd.DataFrame({'date':date_data,'close':close_data})
        close_price = pd_data['close']
        masp_ema = close_price.ewm(span=int(option['disparity_term']), adjust=False).mean()
        arr_close = float(close_price.iloc[-1])
        arr_masp = float(masp_ema.iloc[-1])
        if (arr_masp / arr_close) * 100 > float(option['low_disparity']) and (arr_masp / arr_close) * 100 < float(option['high_disparity']): 
            return_coin.append(coin)
            return_value[0][str(coin).replace("_KRW", "")] = { 'disparity': ((arr_masp / arr_close) * 100), 'disparity_term': option['disparity_term']}
    print("Disparity_condition return_coin :::: ", return_coin)
    return return_coin, return_value