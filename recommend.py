import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc
import numpy as np

# 조건 식에 따른 코인 필터 함수
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

def recommendCoin(options):
    print(options, '=====================================')
    now1 = datetime.datetime.now()

    priceC = ''
    TrasactionC = ''
    DisparityC = ''
    MacdC = ''
    MaspC = ''
    TrendC = ''

    coinList = db.query(models.coinCurrentPrice).all()

    for option in options:
        # 현재 가격 범위 옵션
        if option['option'] =='Price':
            for prc in coinList:
                if float(option['low_price']) < prc.Close and prc.Close < float(option['high_price']):
                    priceC += f'{prc.coin_name} '
                    print(prc.coin_name)

        # 거래대금 가격 범위 옵션
        if option['option'] =='TransactionAmount':
            for trc in coinList:
                if float(option['low_transaction_amount']) < trc.Close and trc.Close < float(option['high_transaction_amount']):
                    TrasactionC += f'{trc.coin_name} '

        # 이동평균 옵션 
        if option['option'] =='MASP':
            term = option['chart_term']
            if term[-1] == 'm':
                bigger = int(option['first_disparity'])
                if bigger < int(option['second_disparity']):
                    bigger = int(option['second_disparity'])

                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(minutes=(bigger * times)))
                findIndex = db.query(models.coinPrice1M).filter(models.coinPrice1M.time.like(f'{time[:-10]}%')).first()
                Maspdf = db.query(models.coinPrice1M).filter(models.coinPrice1M.idx > findIndex.idx).all()

                MaspList = []

                for Masp in Maspdf:
                    MaspList.append({'coin_name':Masp.coin_name, 'time':Masp.time, 'Close':Masp.Close})

                df = pd.DataFrame(MaspList)

                for coin in coinList:
                    try:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]
                        df3 = df2[- int(option['first_disparity']):]
                        df4 = df2[- int(option['second_disparity']):]

                        avgP1 = df3['Close'].mean()
                        Recent1 = df3['Close'].iloc[-1]
                        disP1 = (avgP1 / Recent1) * 100

                        avgP2 = df4['Close'].mean()
                        Recent2 = df4['Close'].iloc[-1]
                        disP2 = (avgP2 / Recent2) * 100

                        if option['comparison'] == '>=':
                            if disP1 >= disP2:
                                MaspC += f'{coin.coin_name} '
                        if option['comparison'] == '<=':
                            if disP1 <= disP2:
                                MaspC += f'{coin.coin_name} '

                    except Exception as e:
                        print(e, coin.coin_name)

            if term[-1] == 'h':
                bigger = int(option['first_disparity'])
                if bigger < int(option['second_disparity']):
                    bigger = int(option['second_disparity'])

                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(minutes=(bigger * times)))
                findIndex = db.query(models.coinPrice1H).filter(models.coinPrice1H.time.like(f'{time[:-12]}%')).first()
                Maspdf = db.query(models.coinPrice1H).filter(models.coinPrice1H.idx > findIndex.idx).all()

                MaspList = []

                for Masp in Maspdf:
                    MaspList.append({'coin_name':Masp.coin_name, 'time':Masp.time, 'Close':Masp.Close})

                df = pd.DataFrame(MaspList)

                for coin in coinList:
                    try:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]
                        df3 = df2[- int(option['first_disparity']):]
                        df4 = df2[- int(option['second_disparity']):]

                        avgP1 = df3['Close'].mean()
                        Recent1 = df3['Close'].iloc[-1]
                        disP1 = (avgP1 / Recent1) * 100

                        avgP2 = df4['Close'].mean()
                        Recent2 = df4['Close'].iloc[-1]
                        disP2 = (avgP2 / Recent2) * 100

                        if option['comparison'] == '>=':
                            if disP1 >= disP2:
                                MaspC += f'{coin.coin_name} '
                        if option['comparison'] == '<=':
                            if disP1 <= disP2:
                                MaspC += f'{coin.coin_name} '

                    except Exception as e:
                        print(e, coin.coin_name)

        if option['option'] =='Disparity':
            term = option['chart_term']
            if term[-1] == 'm':
                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(minutes=int(times) * int(option['disparity_term'])))
                findIndex = db.query(models.coinPrice1M).filter(models.coinPrice1M.time.like(f'{time[:-10]}%')).first()
                disparitydf = db.query(models.coinPrice1M).filter(models.coinPrice1M.idx > findIndex.idx).all()

                disparityList = []

                for disparity in disparitydf:
                    disparityList.append({'coin_name':disparity.coin_name, 'time':disparity.time, 'Close':disparity.Close})

                df = pd.DataFrame(disparityList)
                for coin in coinList:
                    try:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]

                        avgP = df2['Close'].mean()
                        Recent = df2['Close'].iloc[-1]
                        disP = (avgP / Recent) * 100

                        if int(option['low_disparity']) < disP < int(option['high_disparity']):
                            DisparityC += f'{coin.coin_name} '
                    except Exception as e:
                        print(e, coin.coin_name)

            if term[-1] == 'h':
                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(hours=int(times) * int(option['disparity_term'])))
                findIndex = db.query(models.coinPrice1H).filter(models.coinPrice1H.time.like(f'{time[:-12]}%')).first()
                disparitydf = db.query(models.coinPrice1H).filter(models.coinPrice1H.idx > findIndex.idx).all()

                disparityList = []

                for disparity in disparitydf:
                    disparityList.append({'coin_name':disparity.coin_name, 'time':disparity.time, 'Close':disparity.Close})

                df = pd.DataFrame(disparityList)
                for coin in coinList:
                    try:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]

                        avgP = df2['Close'].mean()
                        Recent = df2['Close'].iloc[-1]
                        disP = (avgP / Recent) * 100

                        if int(option['low_disparity']) < disP < int(option['high_disparity']):
                            DisparityC += f'{coin.coin_name} '
                    except Exception as e:
                        print(e, coin.coin_name)

        if option['option'] =='Trend':
            if option['chart_term'][-1] =='m':
                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(minutes=((int(option['trend_term']) + 2) * times)))
                print(time[:-10])
                findIndex = db.query(models.coinPrice1M).filter(models.coinPrice1M.time.like(f'{time[:-10]}%')).first()
                trendDf = db.query(models.coinPrice1M).filter(models.coinPrice1M.idx > findIndex.idx).all()

                TrendList = []

                for trend in trendDf:
                    TrendList.append({'coin_name':trend.coin_name, 'time':trend.time, 'Close':trend.Close, 'Volume':trend.Volume})

                df = pd.DataFrame(TrendList)
                for coin in coinList:
                    df2 = df.loc[df['coin_name'] == coin.coin_name]

                    vol = float(df2['Volume'].sum())
                    if vol == 0.0:
                        continue

                    df3 = df2[(len(df2) % times):]
                    df3.reset_index(drop=True, inplace=True)

                    # 리스트를 times개씩 묶기
                    new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                    z = 0
                    if option['trend_type'] == '상승' and int(option['trend_reverse']) == 0:
                        for i in range(2, len(df3)):
                            if df3['Close'].iloc[i] > df3['Close'].iloc[i-1]:
                                z += 1
                                print('0000000000000000000000000000000000000000000000000000000')
                            else:
                                z = 0

                            if z == int(option['trend_term']):
                                TrendC += f'{coin.coin_name} '

                    if option['trend_type'] == '하락' and int(option['trend_reverse']) == 0:
                        for i in range(2, len(df3)):
                            if df3['Close'].iloc[i] < df3['Close'].iloc[i-1]:
                                z += 1
                            else:
                                z = 0

                            if z == int(option['trend_term']):
                                TrendC += f'{coin.coin_name} '

                    if option['trend_type'] == '상승' and int(option['trend_reverse']) == 1:
                        for i in range(1, len(df3)):
                            if z == int(option['trend_term']):
                                if df3['Close'].iloc[i] < df3['Close'].iloc[i-1]:
                                    TrendC += f'{coin.coin_name} '

                            if df3['Close'].iloc[i] > df3['Close'].iloc[i-1]:
                                z += 1
                            else:
                                z = 0

                    if option['trend_type'] == '하락' and int(option['trend_reverse']) == 1:
                        for i in range(1, len(df3)):
                            if z == int(option['trend_term']):
                                if df3['Close'].iloc[i] > df3['Close'].iloc[i-1]:
                                    TrendC += f'{coin.coin_name} '

                            if df3['Close'].iloc[i] < df3['Close'].iloc[i-1]:
                                z += 1
                            else:
                                z = 0

        # MACD 옵션 
        if option['option'] =='MACD':
            # 분 단위
            if option['chart_term'][-1] =='m':
                # 시간 데이터 부족으로 분단위 데이터 사용 중
                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(minutes=int(option['long_disparity']) * (times + 1)))
                print(time[:-10])
                findIndex = db.query(models.coinPrice1M).filter(models.coinPrice1M.time.like(f'{time[:-10]}%')).first()
                MACDdf = db.query(models.coinPrice1M).filter(models.coinPrice1M.idx > findIndex.idx).all()

                MACDList = []
                for MACD in MACDdf:
                    MACDList.append({'coin_name':MACD.coin_name, 'time':MACD.time, 'Close':MACD.Close, 'Volume':MACD.Volume})

                df = pd.DataFrame(MACDList)

                print(len(df))

                for coin in coinList:
                    df2 = df.loc[df['coin_name'] == coin.coin_name]
                    df2.reset_index(drop=True, inplace=True)

                    df3 = df2[(len(df2) % times):]
                    df3.reset_index(drop=True, inplace=True)

                    vol = df2[int((len(df2) * times) / 2):]
                    if vol['Volume'].sum() == 0.0:
                        continue

                    # 리스트를 times개씩 묶기
                    new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                    # short EMA 계산
                    emashort = new_df['Close'].ewm(span=int(option['short_disparity'])).mean()
                    # long EMA 계산
                    emalong = new_df['Close'].ewm(span=int(option['long_disparity'])).mean()
                    # MACD 계산
                    macd = emashort - emalong

                    if option['up_down'] == '이상':
                        if macd.iloc[-1] >= 0:
                            MacdC += f'{coin.coin_name} '
                    if option['up_down'] == '이하':
                        if macd.iloc[-1] <= 0:
                            MacdC += f'{coin.coin_name} '

            # 시간 단위
            if option['chart_term'][-1] =='h':
                # 시간 데이터 부족으로 분단위 데이터 사용 중
                times = int(option['chart_term'][:-1])
                time = str(datetime.datetime.now() - datetime.timedelta(hours=int(option['long_disparity']) * (times + 1)))
                findIndex = db.query(models.coinPrice1H).filter(models.coinPrice1H.time.like(f'{time[:-12]}%')).first()
                MACDdf = db.query(models.coinPrice1H).filter(models.coinPrice1H.idx > findIndex.idx).all()

                MACDList = []
                for MACD in MACDdf:
                    MACDList.append({'coin_name':MACD.coin_name, 'time':MACD.time, 'Close':MACD.Close, 'Volume':MACD.Volume})

                df = pd.DataFrame(MACDList)

                for coin in coinList:
                    df2 = df.loc[df['coin_name'] == coin.coin_name]
                    df2.reset_index(drop=True, inplace=True)

                    df3 = df2[(len(df2) % times):]
                    df3.reset_index(drop=True, inplace=True)

                    vol = df2[int((len(df2) * times) / 2):]
                    if vol['Volume'].sum() == 0.0:
                        continue

                    # 리스트를 times개씩 묶기
                    new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                    # short EMA 계산
                    emashort = new_df['Close'].ewm(span=int(option['short_disparity'])).mean()
                    # long EMA 계산
                    emalong = new_df['Close'].ewm(span=int(option['long_disparity'])).mean()
                    # MACD 계산
                    macd = emashort - emalong

                    if option['up_down'] == '이상':
                        if macd.iloc[-1] >= 0:
                            MacdC += f'{coin.coin_name} '
                    if option['up_down'] == '이하':
                        if macd.iloc[-1] <= 0:
                            MacdC += f'{coin.coin_name} '


    now2 = datetime.datetime.now()
    print(TrendC, '=====================')

    print(now2 - now1)

    return {'Price': priceC, 'TransactionAmount': TrasactionC, 'Disparity': DisparityC, 'Trend': TrendC, 'MACD': MacdC, 'MASP':MaspC}