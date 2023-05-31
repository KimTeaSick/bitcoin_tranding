import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc
import numpy as np
import asyncio

# 조건 모듈
from recommends import priceFilter
from recommends import transactionAmountFilter
from recommends import MaspFilter

async def recommendCoin(options, mMax, hMax):
        try:
            db = SessionLocal()
            db: Session
        finally:
            db.close()

        print(options, '=====================================')
        now1 = datetime.datetime.now()
        nowstamp = int(int(now1.timestamp()) /60) * 60 + (60*540)
        print(datetime.datetime.utcfromtimestamp(nowstamp))
        print(mMax)

        # 분단위
        mNowStamp = nowstamp - (mMax * 60)
        dfmSource = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= mNowStamp).all()
        dfmList = []
        i = 0
        for dfs in dfmSource:
            i +=1
            dfmList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':dfs.Close, 'Volume':dfs.Volume})

        #시간 단위
        hNowStamp = nowstamp - (hMax * 3600)
        dfhSource = db.query(models.coinPrice1H).filter(models.coinPrice1H.S_time >= hNowStamp).all()
        dfhList = []

        #for dfhl in dfhSource:
            #print(dfhl.S_time)
        print(nowstamp)

        for dfs in dfhSource:
            dfhList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':dfs.Close, 'Volume':dfs.Volume})

        print(i, '9999999999999999999999999999999999999999999999999999999999999999999999999999999999999')

        dfm = pd.DataFrame(dfmList)
        dfh = pd.DataFrame(dfhList)

        coinList = db.query(models.coinCurrentPrice).all()
        coins = []
        coinNames = []

        for coin in coinList:
            coins.append({'name':coin.coin_name, 'Close':coin.Close, 'Transaction_amount':coin.Transaction_amount})
            coinNames.append(coin.coin_name)

        priceL = ''
        TransactionL = ''
        DisparityL = ''
        MacdL = ''
        MaspL = ''
        TrendL = ''

        for option in options:
            # 현재 가격 범위 옵션
            if option['option'] =='Price':
                priceL = priceFilter.priceRecommend(coins, option['low_price'], option['high_price'])

            # 거래대금 가격 범위 옵션
            if option['option'] =='TransactionAmount':
                TransactionL = transactionAmountFilter.transactioAmountRecommend(coins, option['low_transaction_amount'], option['high_transaction_amount'])

            # 이동평균 옵션 
            if option['option'] =='MASP':
                term = option['chart_term']
                if term[-1] == 'm':
                    #MaspL = MaspFilter.MaspRecommend(nowstamp, coinNames, dfmList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    bigger = int(option['first_disparity'])
                    if bigger < int(option['second_disparity']):
                        bigger = int(option['second_disparity'])

                    times = int(option['chart_term'][:-1])
                    time = nowstamp - (bigger * (times + 1) * 60)

                    print(dfm)

                    df = dfm.loc[dfm['S_time'] > time]

                    for coin in coinList:
                        try:
                            df2 = df.loc[df['coin_name'] == coin.coin_name]
                            df3 = df2[- int(option['first_disparity']):]
                            df4 = df2[- int(option['second_disparity']):]

                            vol = df3['Volume'].sum()
                            if vol == 0.0:
                                continue

                            avgP1 = df3['Close'].mean()
                            Recent1 = df3['Close'].iloc[-1]
                            disP1 = (avgP1 / Recent1) * 100

                            avgP2 = df4['Close'].mean()
                            Recent2 = df4['Close'].iloc[-1]
                            disP2 = (avgP2 / Recent2) * 100

                            if option['comparison'] == '>=':
                                if disP1 >= disP2:
                                    MaspL += f'{coin.coin_name} '
                            if option['comparison'] == '<=':
                                if disP1 <= disP2:
                                    MaspL += f'{coin.coin_name} '

                        except Exception as e:
                            print(e, coin.coin_name, option['option'])

                if term[-1] == 'h':
                    #MaspL = MaspFilter.MaspRecommend(nowstamp, coinNames, dfhList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    bigger = int(option['first_disparity'])
                    if bigger < int(option['second_disparity']):
                        bigger = int(option['second_disparity'])

                    times = int(option['chart_term'][:-1])
                    time = nowstamp - (bigger * (times + 1) * 3600)

                    df = dfh.loc[dfh['S_time'] > time]

                    for coin in coinList:
                        try:
                            df2 = df.loc[df['coin_name'] == coin.coin_name]
                            df3 = df2[- int(option['first_disparity']):]
                            df4 = df2[- int(option['second_disparity']):]

                            vol = df3['Volume'].sum()
                            if vol == 0.0:
                                continue

                            avgP1 = df3['Close'].mean()
                            Recent1 = df3['Close'].iloc[-1]
                            disP1 = (avgP1 / Recent1) * 100

                            avgP2 = df4['Close'].mean()
                            Recent2 = df4['Close'].iloc[-1]
                            disP2 = (avgP2 / Recent2) * 100

                            if option['comparison'] == '>=':
                                if disP1 >= disP2:
                                    MaspL += f'{coin.coin_name} '
                            if option['comparison'] == '<=':
                                if disP1 <= disP2:
                                    MaspL += f'{coin.coin_name} '

                        except Exception as e:
                            print(e, coin.coin_name, option['option'])

            if option['option'] =='Disparity':
                term = option['chart_term']
                if term[-1] == 'm':
                    times = int(option['chart_term'][:-1])

                    time = nowstamp - (int(times) * int(option['disparity_term']) * 60)

                    df = dfm.loc[dfm['S_time'] > time]

                    for coin in coinList:
                        #try:

                            df2 = df.loc[df['coin_name'] == coin.coin_name]

                            vol = df2['Volume'].sum()
                            if vol == 0.0:
                                continue

                            avgP = df2['Close'].mean()
                            Recent = df2['Close'].iloc[-1]
                            disP = (Recent / avgP) * 100

                            if int(option['low_disparity']) < disP:
                                if int(option['high_disparity']) > disP :
                                    DisparityL += f'{coin.coin_name} '
                        #except Exception as e:
                            #print(e, coin.coin_name, option['option'])

                if term[-1] == 'h':
                    times = int(option['chart_term'][:-1])

                    time = nowstamp - (int(times) * int(option['disparity_term']) * 3600)

                    df = dfh.loc[dfh['S_time'] > time]

                    for coin in coinList:
                        try:
                            df2 = df.loc[df['coin_name'] == coin.coin_name]

                            vol = df2['Volume'].sum()
                            if vol == 0.0:
                                continue

                            avgP = df2['Close'].mean()
                            Recent = df2['Close'].iloc[-1]
                            disP = (Recent / avgP) * 100

                            if int(option['low_disparity']) + 100 < disP < int(option['high_disparity']) + 100:
                                DisparityL += f'{coin.coin_name} '

                        except Exception as e:
                            print(e, coin.coin_name, option['option'])

            if option['option'] =='Trend':
                term = option['chart_term']
                if term[-1] =='m':
                    times = int(option['chart_term'][:-1])

                    time = nowstamp - ((int(option['trend_term']) + int(option['MASP'])+2) * times * 60)

                    df = dfm.loc[dfm['S_time'] > time]

                    for coin in coinList:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]

                        vol = df2['Volume'].sum()
                        if vol == 0.0:
                            continue

                        df3 = df2[(len(df2) % times):]
                        df3.reset_index(drop=True, inplace=True)

                        # 리스트를 times개씩 묶기
                        new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                        masp = new_df["Close"].rolling(window=int(option['MASP'])).mean()
                        masp.fillna(0)

                        z = 0
                        if option['trend_type'] == 'up_trend' and int(option['trend_reverse']) == 0:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if new_df['Close'][i] > float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                                if z == int(option['trend_term']):
                                    TrendL += f'{coin.coin_name} '

                        if option['trend_type'] == 'down_trend' and int(option['trend_reverse']) == 0:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if new_df['Close'][i] < float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                                if z == int(option['trend_term']):
                                    TrendL += f'{coin.coin_name} '

                        if option['trend_type'] == 'up_trend' and int(option['trend_reverse']) == 1:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if z == int(option['trend_term']):
                                    if new_df['Close'].iloc[i] < float(masp[i]):
                                        TrendL += f'{coin.coin_name} '

                                if new_df['Close'].iloc[i] > float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                        if option['trend_type'] == 'down_trend' and int(option['trend_reverse']) == 1:
                            for i in range(len(new_df)):
                                if z == int(option['trend_term']):
                                    if new_df['Close'].iloc[i] > float(masp[i]):
                                        TrendL += f'{coin.coin_name} '

                                if new_df['Close'].iloc[i] < float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                if term[-1] =='h':
                    times = int(option['chart_term'][:-1])
                    time = str(datetime.datetime.now() - datetime.timedelta(hours=((int(option['trend_term']) + int(option['MASP'])+2) * times)))

                    time = nowstamp - ((int(option['trend_term']) + int(option['MASP'])+2) * times * 3600)

                    df = dfh.loc[dfh['S_time'] > time]

                    for coin in coinList:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]

                        vol = df2['Volume'].sum()
                        if vol == 0.0:
                            continue

                        df3 = df2[(len(df2) % times):]
                        df3.reset_index(drop=True, inplace=True)

                        # 리스트를 times개씩 묶기
                        new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                        masp = new_df["Close"].rolling(window=int(option['MASP'])).mean()
                        masp.fillna(0)

                        z = 0

                        if option['trend_type'] == 'up_trend' and int(option['trend_reverse']) == 0:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if new_df['Close'][i] > float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                                if z == int(option['trend_term']):
                                    TrendL += f'{coin.coin_name} '

                        if option['trend_type'] == 'down_trend' and int(option['trend_reverse']) == 0:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if new_df['Close'][i] < float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                                if z == int(option['trend_term']):
                                    TrendL += f'{coin.coin_name} '

                        if option['trend_type'] == 'up_trend' and int(option['trend_reverse']) == 1:
                            for i in range(len(new_df)):
                                if float(masp[i]) == 0:
                                    continue

                                if z == int(option['trend_term']):
                                    if new_df['Close'].iloc[i] < float(masp[i]):
                                        TrendL += f'{coin.coin_name} '

                                if new_df['Close'].iloc[i] > float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

                        if option['trend_type'] == 'down_trend' and int(option['trend_reverse']) == 1:
                            for i in range(len(new_df)):
                                if z == int(option['trend_term']):
                                    if new_df['Close'].iloc[i] > float(masp[i]):
                                        TrendL += f'{coin.coin_name} '

                                if new_df['Close'].iloc[i] < float(masp[i]):
                                    z += 1
                                else:
                                    z = 0

            # MACD 옵션 
            if option['option'] =='MACD':
                term = option['chart_term']
                # 분 단위
                if term[-1] =='m':
                    # 시간 데이터 부족으로 분단위 데이터 사용 중
                    times = int(term[:-1])

                    time = nowstamp - (int(option['long_disparity']) * (times) * 60)

                    df = dfm.loc[dfm['S_time'] > time]

                    for coin in coinList:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]
                        df2.reset_index(drop=True, inplace=True)

                        df3 = df2[(len(df2) % times):]
                        df3.reset_index(drop=True, inplace=True)

                        vol = df2['Volume'].sum()
                        if vol == 0.0:
                            continue

                        # 리스트를 times개씩 묶기
                        new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                        # short EMA 계산
                        emashort = new_df['Close'].ewm(span=int(option['short_disparity'])).mean()
                        # long EMA 계산
                        emalong = new_df['Close'].ewm(span=int(option['long_disparity'])).mean()
                        # MACD 계산
                        macd = emashort - emalong

                        if option['up_down'] == 'up':
                            if macd.iloc[-1] >= 0:
                                MacdL += f'{coin.coin_name} '

                        if option['up_down'] == 'down':
                            if macd.iloc[-1] <= 0:
                                MacdL += f'{coin.coin_name} '

                # 시간 단위
                if term[-1] =='h':
                    # 시간 데이터 부족으로 분단위 데이터 사용 중
                    times = int(term[:-1])

                    time = nowstamp - (int(option['long_disparity']) * (times) * 3600)

                    df = dfh.loc[dfh['S_time'] > time]

                    for coin in coinList:
                        df2 = df.loc[df['coin_name'] == coin.coin_name]
                        df2.reset_index(drop=True, inplace=True)

                        df3 = df2[(len(df2) % times):]
                        df3.reset_index(drop=True, inplace=True)

                        vol = df2['Volume'].sum()
                        if vol == 0.0:
                            continue


                        # 리스트를 times개씩 묶기
                        new_df = df3.groupby(np.arange(len(df3)) // times).mean(numeric_only=True)

                        # short EMA 계산
                        emashort = new_df['Close'].ewm(span=int(option['short_disparity'])).mean()
                        # long EMA 계산
                        emalong = new_df['Close'].ewm(span=int(option['long_disparity'])).mean()
                        # MACD 계산
                        macd = emashort - emalong

                        if option['up_down'] == 'up':
                            if macd.iloc[-1] >= 0:
                                MacdL += f'{coin.coin_name} '
                        if option['up_down'] == 'down':
                            if macd.iloc[-1] <= 0:
                                MacdL += f'{coin.coin_name} '

        url = "https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()["data"]

        PriceRecommend = priceL
        TrAmtRecommend = TransactionL
        DisparityRecommend = DisparityL
        TrendRecommend = TrendL
        MacdRecommend = MacdL
        MaspRecommend = MaspL

        time = nowstamp - (10 * 60)
        df = dfm.loc[dfm['S_time'] > time]

        recommendCoins = []
        coinList = db.query(models.coinCurrentPrice).all()
        for coin in coinList:
            recommendCoins.append(coin.coin_name)

        recommendCoins = set(recommendCoins) & set(PriceRecommend)
        recommendCoins = set(recommendCoins) & set(TrAmtRecommend)
        recommendCoins = set(recommendCoins) & set(DisparityRecommend)
        recommendCoins = set(recommendCoins) & set(TrendRecommend)
        recommendCoins = set(recommendCoins) & set(MacdRecommend)
        recommendCoins = set(recommendCoins) & set(MaspRecommend)

        # 리턴할 정보 append
        priceDict = []
        TrAmtDict = []
        DisparityDict = []
        MaspDict = []
        TrendDict = []
        MacdDict = []

        recommendDict = []

        for coin in coinList:
            if coin.coin_name in PriceRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]

                priceDict.append({name:data[name]})

            if coin.coin_name in TrAmtRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]

                TrAmtDict.append({name:data[name]})

            if coin.coin_name in MaspRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]

                MaspDict.append({name:data[name]})

            if coin.coin_name in DisparityRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]

                DisparityDict.append({name:data[name]})

            if coin.coin_name in TrendRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]

                TrendDict.append({name:data[name]})

            if coin.coin_name in MacdRecommend:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]
                MacdDict.append({name:data[name]})

            if coin.coin_name in recommendCoins:
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                #if len(df2) < 5:
                    #continue

                name = coin.coin_name[:-4]
                data[name]['tenRow'] = [df2.to_dict()]
                print(coin.coin_name)

                recommendDict.append({name:data[name]})

        now2 = datetime.datetime.now()
        print(now2 - now1)
        print(PriceRecommend,'4444444444444444444444444444444444444444')
        return {'recommends': recommendDict, 'Price':priceDict, 'TransactioAmount':TrAmtDict, 'Disparity':DisparityDict, 'Masp':MaspDict, 'Trend': TrendDict, 'MACD': MacdDict}