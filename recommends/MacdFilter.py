import pandas as pd
import numpy as np
import time
import requests

# macd 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def MacdRecommend(nowstamp, coinList, dfList, chart_term, short_disparity, long_disparity, signal,  up_down):
    print('-----------------------------------------------------------------------------------------------------------')
    print('macd start ::::::: ')
    print('before condition pass coins ::::::: ', len(coinList))
    print('paramater ::::::: ', nowstamp, chart_term, short_disparity, long_disparity, signal,  up_down)

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

            df["MACD_short"]=df["종가"].ewm(span=int(short_disparity)).mean()
            df["MACD_long"]=df["종가"].ewm(span=int(long_disparity)).mean()
            df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
            df["MACD_signal"]=df["MACD"].ewm(span=int(signal)).mean()  
            df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)
            df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)

            # 상승, 하락 비교
            if len(df) != 0 and up_down == 'up':
                if float(df.iloc[-2]["MACD_oscillator"]) >= 0:
                    Macd_list.append(coin)
                    Macd_value.append({'coin_name':coin, 'macd_short': df.iloc[-2]["MACD_short"], 'macd_long':df.iloc[-2]["MACD_long"], 'macd':df.iloc[-2]["MACD"], 'macd_signal':df.iloc[-2]["MACD_signal"]})

            if len(df) != 0 and up_down == 'down':
                if float(df.iloc[-2]["MACD_oscillator"]) <= 0:
                    Macd_list.append(coin)
                    Macd_value.append({'coin_name':coin, 'macd_short': df.iloc[-2]["MACD_short"], 'macd_long':df.iloc[-2]["MACD_long"], 'macd':df.iloc[-2]["MACD"], 'macd_signal':df.iloc[-2]["MACD_signal"]})

        except Exception as e:
            print(e)
            
    print('macd end ::::::: ', len(Macd_list))
    print('-----------------------------------------------------------------------------------------------------------')

    return Macd_list, Macd_value
