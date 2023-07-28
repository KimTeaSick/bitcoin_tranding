import pandas as pd
import numpy as np
import requests
import datetime
import time

# macd 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def MacdRecommend(nowstamp, coinList, dfList, chart_term, short_disparity, long_disparity, signal,  up_down):
    print('-----------------------------------------------------------------------------------------------------------')
    print('macd start ::::::: ')
    print('paramater ::::::: ', nowstamp, chart_term, short_disparity, long_disparity, signal,  up_down)
    print('before condition pass coins ::::::: ', len(coinList))

    fn_start = datetime.datetime.now()
    Macd_list = []
    Macd_value = []

    # 기준시간 찾기
    times = int(chart_term[:-1])
    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        try:
            #df3 = df2.loc[df['coin_name'] == coin].copy()
            data=requests.get(f'https://api.bithumb.com/public/candlestick/{coin}/1h')
            data=data.json()
            data=data.get("data")
            df=pd.DataFrame(data)

            # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
            df = df[(len(df) % times):]
            df.reset_index(drop=True, inplace=True)
            df.rename(columns={0:'time', 1:"시가", 2:"종가", 3:"고가", 4:"저가", 5:"거래량"}, inplace=True)
            df=df[['time', "시가", "종가", "고가", "저가", "거래량"]].astype("float")
            df.sort_values("time", inplace=True)
            df=df[['time', "시가", "종가", "고가", "저가", "거래량"]].astype("float")
            df.reset_index(drop=True, inplace=True)
            df["date"]=df["time"].apply(lambda x:time.strftime('%Y-%m-%d %H:%M', time.localtime(x/1000)))
            # 리스트를 times개씩 묶기
            df = df.groupby(np.arange(len(df)) // int(chart_term[:-1])).mean(numeric_only=True)
            close_price = df['종가']
            short_ema = close_price.ewm(span=int(short_disparity), adjust=False).mean()
            long_ema = close_price.ewm(span=int(long_disparity), adjust=False).mean()
            macd_line = short_ema - long_ema
            signal_line = macd_line.ewm(span=int(signal), adjust=False).mean()

            if len(df) != 0 and up_down == 'up':
                if float(signal_line.iloc[-1]) > float(macd_line.iloc[-1]):
                    Macd_list.append(coin)
                    Macd_value.append({'coin_name':coin, 'macd_short': short_ema.iloc[-2], 'macd_long':long_ema.iloc[-2], 'macd':macd_line.iloc[-2], 'macd_signal':signal_line.iloc[-2]})
            if len(df) != 0 and up_down == 'down':
                if float(signal_line.iloc[-1]) > float(macd_line.iloc[-1]):
                    Macd_list.append(coin)
                    Macd_value.append({'coin_name':coin, 'macd_short': short_ema.iloc[-2], 'macd_long':long_ema.iloc[-2], 'macd':macd_line.iloc[-2], 'macd_signal':signal_line.iloc[-2]})

        except Exception as e:
            print("MACD Error ::: ::: ", e)
    fn_end = datetime.datetime.now()
    print('macd spend time ::::::: ', fn_end - fn_start)
    print('macd end ::::::: ', len(Macd_list))
    print('-----------------------------------------------------------------------------------------------------------')

    return Macd_list, Macd_value
