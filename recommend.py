import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc
import numpy as np
import asyncio
from sql import *
from dbConnection import MySql

# 조건 모듈
from recommends import priceFilter
from recommends import transactionAmountFilter
from recommends import MaspFilter
from recommends import trendFilter
from recommends import disparityFilter
from recommends import MacdFilter
mysql = MySql()
async def recommendCoin(options, mMax, hMax):
        try:
            db = SessionLocal()
            db: Session
        finally:
            db.close()

        print('options ::::::: ',options, '=====================================')
        # pc 시간, db에 쌓인 유닉스 시간, 비교 필수
        await mysql.AllDelete(deleteSearchCoinListSql)
        now1 = datetime.datetime.now()
        nowstamp = int(int(now1.timestamp()) /60) * 60 #+ (60*540)
        print(datetime.datetime.utcfromtimestamp(nowstamp), 'now-------------------------------------------------------------------------')
        print(hMax, 'hMax')

        # 분단위
        mNowStamp = nowstamp - (mMax * 60)
        dfmSource = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= mNowStamp).all()
        dfmList = []
        i = 0
        for dfs in dfmSource:
            i +=1
            dfmList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':(dfs.Close), 'Volume':dfs.Volume, 'Transaction_amount':dfs.Transaction_amount})

        #시간 단위
        hNowStamp = nowstamp - (hMax * 3600)
        #dfhSource = db.query(models.coinPrice1H).filter(models.coinPrice1H.S_time >= hNowStamp).all()
        dfhSource = db.query(models.coin1HPrice).filter(models.coin1HPrice.STime >= hNowStamp).all()
        dfhList = []

        #for dfhl in dfhSource:
            #print(dfhl.S_time)
        print(nowstamp)

        for dfs in dfhSource:
            #dfhList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':dfs.Close, 'Volume':dfs.Volume, 'Transaction_amount':dfs.Transaction_amount})
            dfhList.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':int(dfs.STime), 'time':dfs.time, 'Close':float(dfs.Close), 'Volume':float(dfs.Volume), 'Transaction_amount':float(dfs.Close) * float(dfs.Volume)})

        coinList = db.query(models.coinList).all()
        #coins = []
        coinNames = []

        for coin in coinList:
            #coins.append({'name':coin.coin_name, 'Close':coin.Close, 'Transaction_amount':coin.Transaction_amount})
            coinNames.append(coin.coin_name)

        priceL = []
        TransactionL = []
        DisparityL = []
        MacdL = []
        MaspL = []
        TrendL = []

        priceValue = []
        transactionAmountValue = []
        MaspValue = []
        DisparityValue = []
        TrendValue = []
        MacdValue = []

        for option in options:
            print(option['option'])
            # 현재 가격 범위 옵션
            if option['option'] =='Price':
                priceL, priceValue = priceFilter.priceRecommend(nowstamp, coinNames, dfmList, option['low_price'], option['high_price'])
                coinNames = set(coinNames) & set(priceL)

            # 거래대금 가격 범위 옵션
            if option['option'] =='TransactionAmount':
                term = option['chart_term']
                if term[-1] == 'm':
                    TransactionL, transactionAmountValue = transactionAmountFilter.transactioAmountRecommend(nowstamp, coinNames, dfmList,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coinNames = set(coinNames) & set(TransactionL)

                if term[-1] == 'h':
                    TransactionL, transactionAmountValue = transactionAmountFilter.transactioAmountRecommend(nowstamp, coinNames, dfhList,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coinNames = set(coinNames) & set(TransactionL)

            # 이동평균 옵션 
            if option['option'] =='MASP':
                term = option['chart_term']
                if term[-1] == 'm':
                    MaspL, MaspValue = MaspFilter.MaspRecommend(nowstamp, coinNames, dfmList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coinNames = set(coinNames) & set(MaspL)

                if term[-1] == 'h':
                    MaspL, MaspValue = MaspFilter.MaspRecommend(nowstamp, coinNames, dfhList, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coinNames = set(coinNames) & set(MaspL)

            # 이격도 옵션
            if option['option'] =='Disparity':
                term = option['chart_term']
                if term[-1] == 'm':
                    DisparityL, DisparityValue = disparityFilter.disparityRecommend(nowstamp, coinNames, dfmList, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coinNames = set(coinNames) & set(DisparityL)

                if term[-1] == 'h':
                    DisparityL, DisparityValue = disparityFilter.disparityRecommend(nowstamp, coinNames, dfhList, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coinNames = set(coinNames) & set(DisparityL)

            # 추세 옵션
            if option['option'] =='Trend':
                term = option['chart_term']
                if term[-1] =='m':
                    TrendL, TrendValue = trendFilter.trendRecommend(nowstamp, coinNames, dfmList, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coinNames = set(coinNames) & set(TrendL)

                if term[-1] =='h':
                    TrendL, TrendValue = trendFilter.trendRecommend(nowstamp, coinNames, dfhList, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coinNames = set(coinNames) & set(TrendL)
                    print(TrendValue)

            # MACD 옵션 
            if option['option'] =='MACD':
                term = option['chart_term']
                # 분 단위
                if term[-1] =='m':
                    MacdL, MacdValue = MacdFilter.MacdRecommend(nowstamp, coinNames, dfmList, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                    coinNames = set(coinNames) & set (MacdL)

                # 시간 단위
                if term[-1] =='h':
                    MacdL, MacdValue = MacdFilter.MacdRecommend(nowstamp, coinNames, dfhList, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                    coinNames = set(coinNames) & set (MacdL)
                    print(MacdValue)

        url = "https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()["data"]


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
                coinPriceValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, priceValue))

                newDict = data[name]
                newDict['price'] = coinPriceValue[0]['price']
                priceDict.append({name:newDict})

            if coin.coin_name in TransactionL:
                name = coin.coin_name[:-4]
                coinTransactionAmountValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, transactionAmountValue))

                newDict = data[name]
                newDict['Transaction_amount'] = coinTransactionAmountValue[0]['Transaction_amount']
                TrAmtDict.append({name:newDict})

            if coin.coin_name in MaspL:
                name = coin.coin_name[:-4]
                coinMaspValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, MaspValue))

                newDict = data[name]
                newDict['first_disparity'] = coinMaspValue[0]['first_disparity']
                newDict['second_disparity'] = coinMaspValue[0]['second_disparity']

                MaspDict.append({name:newDict})

            if coin.coin_name in DisparityL:
                name = coin.coin_name[:-4]
                coinDisparityValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, DisparityValue))

                newDict = data[name]
                newDict['disparity'] = coinDisparityValue[0]['disparity']

                DisparityDict.append({name:newDict})

            if coin.coin_name in TrendL:
                name = coin.coin_name[:-4]
                coinTrendValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, TrendValue))

                newDict = data[name]
                newDict['first_value'] = coinTrendValue[0]['first_value']
                newDict['last_value'] = coinTrendValue[0]['last_value']
                TrendDict.append({name:newDict})

            if coin.coin_name in MacdL:
                name = coin.coin_name[:-4]
                coinMacdValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, MacdValue))

                newDict = data[name]
                newDict['macd_short'] = coinMacdValue[0]['macd_short']
                newDict['macd_long'] = coinMacdValue[0]['macd_long']
                newDict['macd'] = coinMacdValue[0]['macd']
                newDict['macd_signal'] = coinMacdValue[0]['macd_signal']
                MacdDict.append({name:newDict})

            if coin.coin_name in coinNames:
                name = coin.coin_name[:-4]

                recommendDict.append({name:data[name]})

        now2 = datetime.datetime.now()
        print(now2 - now1)

        db.close()
        print(len(coinNames))
        insertList = []
        print("recommendDict.keys() ::::::::::::::: ", recommendDict)
        print("recommendDict.__len__ ::::::::::::::: ", len(recommendDict))
        if len(recommendDict) != 0:
            for coin in recommendDict:
                coinKey = list(coin.keys())
                coinValue = list(coin.values())
                insertList.append({'name':coinKey[0], 'price':coinValue[0]['closing_price']})
                coinValue[0]['closing_price']
                coinKey[0]
                mysql.Insert(insertSearchCoinListSql,[coinKey[0], coinValue[0]['closing_price']])
            print('insertList ::::::::: ', insertList)

        return {'recommends': recommendDict, 'Price':priceDict, 'TransactioAmount':TrAmtDict, 'Masp':MaspDict, 'Trend': TrendDict, 'Disparity':DisparityDict, 'MACD': MacdDict}