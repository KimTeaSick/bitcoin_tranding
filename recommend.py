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
from recommends import trendFilter
from recommends import disparityFilter
from recommends import MacdFilter

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
        print(hMax, 'hMax')


        # 분단위
        mNowStamp = nowstamp - (mMax * 60)
        dfmSource = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= mNowStamp).all()
        dfmList = []
        i = 0
        for dfs in dfmSource:
            i +=1
            dfmList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':dfs.Close, 'Volume':dfs.Volume, 'Transaction_amount':dfs.Transaction_amount})

        #시간 단위
        hNowStamp = nowstamp - (hMax * 3600)
        dfhSource = db.query(models.coinPrice1H).filter(models.coinPrice1H.S_time >= hNowStamp).all()
        dfhList = []

        #for dfhl in dfhSource:
            #print(dfhl.S_time)
        print(nowstamp)

        for dfs in dfhSource:
            dfhList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':dfs.Close, 'Volume':dfs.Volume, 'Transaction_amount':dfs.Transaction_amount})

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
            print(option['option'])
            # 현재 가격 범위 옵션
            if option['option'] =='Price':
                priceL = priceFilter.priceRecommend(nowstamp, coinNames, dfmList, option['low_price'], option['high_price'])
                coinNames = set(coinNames) & set(priceL)

            # 거래대금 가격 범위 옵션
            if option['option'] =='TransactionAmount':
                term = option['chart_term']
                if term[-1] == 'm':
                    TransactionL = transactionAmountFilter.transactioAmountRecommend(nowstamp, coinNames, dfmList,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coinNames = set(coinNames) & set(TransactionL)

                if term[-1] == 'h':
                    TransactionL = transactionAmountFilter.transactioAmountRecommend(nowstamp, coinNames, dfhList,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coinNames = set(coinNames) & set(TransactionL)

            # 이동평균 옵션 
            if option['option'] =='MASP':
                term = option['chart_term']
                if term[-1] == 'm':
                    MaspL = MaspFilter.MaspRecommend(nowstamp, coinNames, dfmList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coinNames = set(coinNames) & set(MaspL)

                if term[-1] == 'h':
                    MaspL = MaspFilter.MaspRecommend(nowstamp, coinNames, dfhList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coinNames = set(coinNames) & set(MaspL)

            # 이격도 옵션
            if option['option'] =='Disparity':
                term = option['chart_term']
                if term[-1] == 'm':
                    DisparityL = disparityFilter.disparityRecommend(nowstamp, coinNames, dfmList, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coinNames = set(coinNames) & set(DisparityL)

                if term[-1] == 'h':
                    DisparityL = disparityFilter.disparityRecommend(nowstamp, coinNames, dfhList, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coinNames = set(coinNames) & set(DisparityL)

            # 추세 옵션
            if option['option'] =='Trend':
                term = option['chart_term']
                if term[-1] =='m':
                    TrendL = trendFilter.trendRecommend(nowstamp, coinNames, dfmList, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coinNames = set(coinNames) & set(TrendL)

                if term[-1] =='h':
                    TrendL = trendFilter.trendRecommend(nowstamp, coinNames, dfhList, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coinNames = set(coinNames) & set(TrendL)

            # MACD 옵션 
            if option['option'] =='MACD':
                term = option['chart_term']
                # 분 단위
                if term[-1] =='m':
                    MacdL = MacdFilter.MacdRecommend(nowstamp, coinNames, dfmList, term, option['short_disparity'], option['long_disparity'], option['up_down'])
                    coinNames = set(coinNames) & set (MacdL)

                # 시간 단위
                if term[-1] =='h':
                    MacdL = MacdFilter.MacdRecommend(nowstamp, coinNames, dfhList, term, option['short_disparity'], option['long_disparity'], option['up_down'])
                    coinNames = set(coinNames) & set (MacdL)

        url = "https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()["data"]

        '''
        PriceRecommend = priceL
        TrAmtRecommend = TransactionL
        DisparityRecommend = DisparityL
        TrendRecommend = TrendL
        MacdRecommend = MacdL
        MaspRecommend = MaspL'''

        recommendCoins = []
        coinList = db.query(models.coinCurrentPrice).all()
        for coin in coinList:
            recommendCoins.append(coin.coin_name)

        '''
        # 조건 모두 만족하는 코인 (수정예정)
        recommendCoins = set(recommendCoins) & set(priceL)
        recommendCoins = set(recommendCoins) & set(TransactionL)
        recommendCoins = set(recommendCoins) & set(DisparityL)
        recommendCoins = set(recommendCoins) & set(TrendL)
        recommendCoins = set(recommendCoins) & set(MacdL)
        recommendCoins = set(recommendCoins) & set(MaspL)'''

        # 리턴할 정보 append
        priceDict = []
        TrAmtDict = []
        DisparityDict = []
        MaspDict = []
        TrendDict = []
        MacdDict = []

        recommendDict = []

        # 코인별 조건에 맞는 지 찾고 api 현재가격 정보, 최근 10개 정보 return
        for coin in coinList:
            if coin.coin_name in priceL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''
                try:
                    priceDict.append({name:data[name]})
                except Exception as e:
                    print(e)

            if coin.coin_name in TransactionL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''
                TrAmtDict.append({name:data[name]})

            if coin.coin_name in MaspL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''
                MaspDict.append({name:data[name]})

            if coin.coin_name in DisparityL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''
                DisparityDict.append({name:data[name]})

            if coin.coin_name in TrendL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''
                TrendDict.append({name:data[name]})

            if coin.coin_name in MacdL:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)
                
                data[name]['tenRow'] = [df2.to_dict()]'''
                MacdDict.append({name:data[name]})

            if coin.coin_name in coinNames:
                name = coin.coin_name[:-4]
                '''
                df2 = df.loc[df['coin_name'] == coin.coin_name]
                df2.reset_index(drop=True, inplace=True)

                data[name]['tenRow'] = [df2.to_dict()]
                '''

                recommendDict.append({name:data[name]})

        now2 = datetime.datetime.now()
        print(now2 - now1)

        db.close()
        print(len(coinNames))
        return {'recommends': recommendDict, 'Price':priceDict, 'TransactioAmount':TrAmtDict, 'Masp':MaspDict, 'Trend': TrendDict, 'Disparity':DisparityDict, 'MACD': MacdDict}