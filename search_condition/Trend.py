import pandas as pd

def Trend_condition(coin_name, data):
    trend_term = 15
    close_price = data['close']

    masp_ema = close_price.ewm(span=trend_term, adjust=False).mean()

    trend_data = pd.DataFrame({
      'Name': coin_name,
      'masp': masp_ema,
    })
    
    arr_data = list(trend_data['masp'].iloc[-6:])
    
    print("arr_data :::: ",coin_name, arr_data)
    # for i in range(5):
    #   diff = arr_data[i] - arr_data[i - 1]
    #   print("diff :::: ",coin_name, diff)
      