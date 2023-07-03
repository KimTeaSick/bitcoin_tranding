import pandas as pd
import numpy as np
import time
import requests

'''
# macd 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def MacdRecommend(nowstamp, coinList, dfList, chart_term, short_disparity, long_disparity, signal,  up_down):
    MacdL = []
    MacdValue = []
    print('macd:', len(coinList))
    print(nowstamp, chart_term, short_disparity, long_disparity, signal,  up_down)

    # 기준시간 찾기
    times = int(chart_term[:-1])
    if chart_term[-1] == 'm':
        macTime = nowstamp - ((int(long_disparity) + int(signal)) * (times) * 60)
    if chart_term[-1] == 'h':
        macTime = nowstamp - ((int(long_disparity) + int(signal)) * (times) * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    df['date'] = pd.to_datetime(df['time'])

    df2 = df.loc[df['S_time'] > macTime]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        df3 = df2.loc[df['coin_name'] == coin].copy()

        df3.loc[:, 'time'] = pd.to_datetime(df3['time'])
        df3.index = pd.to_datetime(df3['time'])
        df3 = df3[~df3.index.duplicated(keep='first')]
        df3.reset_index(drop=True, inplace=True)

        df3 = df3.set_index('time').resample('1H').asfreq()
        df3 = df3.fillna(method='ffill')

        # 시간 범위 내 거래량 0인 코인 빼기
        vol = df3['Volume'].sum()
        if vol == 0.0:
            continue

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df4 = df3[(len(df3) % times):]
        df4.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

        # short EMA 계산
        emashort = df['Close'].ewm(span=int(short_disparity)).mean()
        # long EMA 계산
        emalong = df['Close'].ewm(span=int(long_disparity)).mean()
        # MACD 계산
        macd = emashort - emalong
        macdSignal = macd.ewm(span=int(signal)).mean()
        macdOscillator = macd - macdSignal

        # 상승, 하락 비교
        if len(df3) != 0 and up_down == 'up':
            if float(macdOscillator.iloc[-1]) >= 0:
                MacdL.append(coin)
                MacdValue.append({'coin_name':coin, 'macd_short': emashort.iloc[-1], 'macd_long':emalong.iloc[-1], 'macd':macd.iloc[-1], 'macd_signal':macdSignal.iloc[-1]})

        if len(df3) != 0 and up_down == 'down':
            if float(macdOscillator.iloc[-1]) <= 0:
                MacdL.append(coin)
                MacdValue.append({'coin_name':coin, 'macd_short': emashort.iloc[-1], 'macd_long':emalong.iloc[-1], 'macd':macd.iloc[-1], 'macd_signal':macdSignal.iloc[-1]})
'''


# macd 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def MacdRecommend(nowstamp, coinList, dfList, chart_term, short_disparity, long_disparity, signal,  up_down):
    MacdL = []
    MacdValue = []
    print('macd:', len(coinList))
    print(nowstamp, chart_term, short_disparity, long_disparity, signal,  up_down)

    # 기준시간 찾기
    times = int(chart_term[:-1])
    if chart_term[-1] == 'm':
        macTime = nowstamp - ((int(long_disparity) + int(signal)) * (times) * 60)
    if chart_term[-1] == 'h':
        macTime = nowstamp - ((int(long_disparity) + int(signal)) * (times) * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    df['date'] = pd.to_datetime(df['time'])

    df2 = df.loc[df['S_time'] > macTime]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        #df3 = df2.loc[df['coin_name'] == coin].copy()
        data=requests.get(f'https://api.bithumb.com/public/candlestick/{coin}/{chart_term}')
        data=data.json()
        data=data.get("data")
        df=pd.DataFrame(data)

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df = df[(len(df) % times):]
        df.reset_index(drop=True, inplace=True)
        df.rename(columns={0:'time',1:"시가", 2:"종가", 3:"고가",4:"저가",5:"거래량"}, inplace=True)

        df.sort_values("time", inplace=True)
        df=df[['time',"시가", "종가", "고가","저가","거래량"]].astype("float")
        df.reset_index(drop=True, inplace=True)
        df["date"]=df["time"].apply(lambda x:time.strftime('%Y-%m-%d %H:%M', time.localtime(x/1000)))

        # 리스트를 times개씩 묶기
        df = df.groupby(np.arange(len(df)) // times).mean(numeric_only=True)

        df["MACD_short"]=df["종가"].ewm(span=short_disparity).mean()
        df["MACD_long"]=df["종가"].ewm(span=long_disparity).mean()
        df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
        df["MACD_signal"]=df["MACD"].ewm(span=signal).mean()  
        df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)
        df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)

        '''
        df3.sort_values("S_time", inplace=True)
        df3.reset_index(drop=True, inplace=True)
        df3["date"]=df3["S_time"].apply(lambda x:time.strftime('%Y-%m-%d %H:%M', time.localtime(x/1000)))

        # 시간 범위 내 거래량 0인 코인 빼기
        vol = df3['Volume'].sum()
        if vol == 0.0:
            continue

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df4 = df3[(len(df3) % times):]
        df4.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

        df["MACD_short"]=df["Close"].ewm(span=int(short_disparity)).mean()
        df["MACD_long"]=df["Close"].ewm(span=int(long_disparity)).mean()
        df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
        df["MACD_signal"]=df["MACD"].ewm(span=signal).mean()  
        df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)
        df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)
        '''
        '''
        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df4 = df3[(len(df3) % times):]
        df4.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

        # short EMA 계산
        emashort = df['Close'].ewm(span=int(short_disparity)).mean()
        # long EMA 계산
        emalong = df['Close'].ewm(span=int(long_disparity)).mean()
        # MACD 계산
        macd = emashort - emalong
        macdSignal = macd.ewm(span=int(signal)).mean()
        macdOscillator = macd - macdSignal
        '''
        # 상승, 하락 비교
        if len(df) != 0 and up_down == 'up':
            if float(df.iloc[-2]["MACD_oscillator"]) >= 0:
                MacdL.append(coin)
                MacdValue.append({'coin_name':coin, 'macd_short': df.iloc[-2]["MACD_short"], 'macd_long':df.iloc[-2]["MACD_long"], 'macd':df.iloc[-2]["MACD"], 'macd_signal':df.iloc[-2]["MACD_signal"]})

        if len(df) != 0 and up_down == 'down':
            if float(df.iloc[-2]["MACD_oscillator"]) <= 0:
                MacdL.append(coin)
                MacdValue.append({'coin_name':coin, 'macd_short': df.iloc[-2]["MACD_short"], 'macd_long':df.iloc[-2]["MACD_long"], 'macd':df.iloc[-2]["MACD"], 'macd_signal':df.iloc[-2]["MACD_signal"]})


    print(MacdValue, '000000000000000000000000000000000000000000000000000000000000000000000')
    return MacdL, MacdValue
