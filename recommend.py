import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc
import asyncio
import numpy as np
from sqld import *
from dbConnection import MySql
# 조건 모듈
from recommends import priceFilter
from recommends import transactionAmountFilter
from recommends import MaspFilter
from recommends import trendFilter
from recommends import disparityFilter
from recommends import MacdFilter

mysql = MySql()
async def recommendCoin(options, minute_Max, hour_Max):
        try:
            db = SessionLocal()
            db: Session
        finally:
            db.close()

        print('options ::::::: ', options)
        # pc 시간, db에 쌓인 유닉스 시간, 비교 필수
        print('-----------------------------------------------------------------------------------------------------------')
        
        now1 = datetime.datetime.now()
        nowstamp = int(int(now1.timestamp()) /60) * 60 #+ (60*540)

        print('now ::: ::: ',datetime.datetime.utcfromtimestamp(nowstamp))
        print('-----------------------------------------------------------------------------------------------------------')
        # 분단위
        print('minute_Max ::::::: ', minute_Max)
        minute_now_stamp = nowstamp - (minute_Max * 60)
        df_minute_source = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= minute_now_stamp).all()
        df_minute_list = []
        i = 0

        print("df_minute_source start ::::::: ")
        for dfs in df_minute_source:
            i +=1
            df_minute_list.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':dfs.S_time, 'time':dfs.time, 'Close':(dfs.Close), 'Volume':dfs.Volume, 'Transaction_amount':dfs.Transaction_amount})

        print("df_minute_list ::::::: ", len(df_minute_list))

        print('-----------------------------------------------------------------------------------------------------------')

        #시간 단위
        print('hour_Max ::::::: ', hour_Max)
        hour_now_stamp = nowstamp - (hour_Max * 3600)
        df_hour_source = db.query(models.coin1HPrice).filter(models.coin1HPrice.STime >= hour_now_stamp).all()
        df_hour_list = []
        print("df_hour_source start ::::::: ")
        for dfs in df_hour_source:
            df_hour_list.append({'idx':dfs.idx, 'coin_name':dfs.coin_name,'S_time':int(dfs.STime), 'time':dfs.time, 'Close':float(dfs.Close), 'Volume':float(dfs.Volume), 'Transaction_amount':float(dfs.Close) * float(dfs.Volume)})
        print("df_hour_list ::::::: ", len(df_hour_list))
        print('-----------------------------------------------------------------------------------------------------------')
        #coins = []
        coinList = db.query(models.coinList).filter(models.coinList.warning == 0).all()
        coin_name_list = []
        current_coin = db.query(models.coinCurrentPrice).all()

        for current in current_coin:
            df_hour_list.append({'coin_name':current.coin_name,'S_time':int(current.S_time), 'time':current.time, 'Close':float(current.Close), 'Volume':float(0.0), 'Transaction_amount':float(current.Close) * float(0.0)})

        for coin in coinList:
            #coins.append({'name':coin.coin_name, 'Close':coin.Close, 'Transaction_amount':coin.Transaction_amount})
            coin_name_list.append(coin.coin_name)

        price_list = []
        Transaction_list = []
        Disparity_list = []
        Macd_list = []
        Masp_list = []
        Trend_list = []

        priceValue = []
        transactionAmountValue = []
        MaspValue = []
        DisparityValue = []
        TrendValue = []
        MacdValue = []

        for option in options:
            print("option ::::::: ", option['option'])
            print('-----------------------------------------------------------------------------------------------------------')
            # 현재 가격 범위 옵션
            if option['option'] == 'Price':
                price_list, priceValue = priceFilter.priceRecommend(nowstamp, coin_name_list, df_minute_list, option['low_price'], option['high_price'])
                coin_name_list = set(coin_name_list) & set(price_list)
                print("coin_name_list = set(coin_name_list) & set(price_list)", coin_name_list)

            # 거래대금 가격 범위 옵션
            if option['option'] == 'TransactionAmount':
                term = option['chart_term']
                if term[-1] == 'm':
                    Transaction_list, transactionAmountValue = transactionAmountFilter.transactioAmountRecommend(nowstamp, coin_name_list, df_minute_list,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coin_name_list = set(coin_name_list) & set(Transaction_list)

                if term[-1] == 'h':
                    Transaction_list, transactionAmountValue = transactionAmountFilter.transactioAmountRecommend(nowstamp, coin_name_list, df_hour_list,  option['chart_term'], option['low_transaction_amount'], option['high_transaction_amount'])
                    coin_name_list = set(coin_name_list) & set(Transaction_list)
            print("Transaction_list = set(coin_name_list) & set(price_list)", coin_name_list)

            # 이동평균 옵션 
            if option['option'] == 'MASP':
                term = option['chart_term']
                if term[-1] == 'm':
                    Masp_list, MaspValue = MaspFilter.MaspRecommend(nowstamp, coin_name_list, df_minute_list, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coin_name_list = set(coin_name_list) & set(Masp_list)

                if term[-1] == 'h':
                    Masp_list, MaspValue = MaspFilter.MaspRecommend(nowstamp, coin_name_list, df_hour_list, option['chart_term'], option['first_disparity'], option['second_disparity'], option['comparison'])
                    coin_name_list = set(coin_name_list) & set(Masp_list)

            # 이격도 옵션
            if option['option'] == 'Disparity':
                term = option['chart_term']
                if term[-1] == 'm':
                    Disparity_list, DisparityValue = disparityFilter.disparityRecommend(nowstamp, coin_name_list, df_minute_list, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coin_name_list = set(coin_name_list) & set(Disparity_list)

                if term[-1] == 'h':
                    Disparity_list, DisparityValue = disparityFilter.disparityRecommend(nowstamp, coin_name_list, df_hour_list, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                    coin_name_list = set(coin_name_list) & set(Disparity_list)

            # 추세 옵션
            if option['option'] == 'Trend':
                term = option['chart_term']
                if term[-1] =='m':
                    Trend_list, TrendValue = trendFilter.trendRecommend(nowstamp, coin_name_list, df_minute_list, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coin_name_list = set(coin_name_list) & set(Trend_list)

                if term[-1] =='h':
                    Trend_list, TrendValue = trendFilter.trendRecommend(nowstamp, coin_name_list, df_hour_list, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                    coin_name_list = set(coin_name_list) & set(Trend_list)

            # MACD 옵션 
            if option['option'] == 'MACD':
                term = option['chart_term']
                # 분 단위
                if term[-1] =='m':
                    Macd_list, MacdValue = MacdFilter.MacdRecommend(nowstamp, coin_name_list, df_minute_list, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                    coin_name_list = set(coin_name_list) & set (Macd_list)

                # 시간 단위
                if term[-1] =='h':
                    Macd_list, MacdValue = MacdFilter.MacdRecommend(nowstamp, coin_name_list, df_hour_list, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                    coin_name_list = set(coin_name_list) & set (Macd_list)

        url = "https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()["data"]

        # 리턴할 정보 append
        Price_dict = []
        TA_dict = []
        Disparity_dict = []
        Masp_dict = []
        Trend_dict = []
        Macd_dict = []

        recommend_dict = []

        # 코인별 조건에 맞는 지 찾고 api 현재가격 정보, 최근 10개 정보 return
        for coin in coinList:
            if coin.coin_name in price_list:
                name = coin.coin_name[:-4]
                coinPriceValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, priceValue))

                newDict = data[name]
                newDict['price'] = coinPriceValue[0]['price']
                Price_dict.append({name:newDict})

            if coin.coin_name in Transaction_list:
                name = coin.coin_name[:-4]
                coinTransactionAmountValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, transactionAmountValue))

                newDict = data[name]
                newDict['Transaction_amount'] = coinTransactionAmountValue[0]['Transaction_amount']
                TA_dict.append({name:newDict})

            if coin.coin_name in Masp_list:
                name = coin.coin_name[:-4]
                coinMaspValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, MaspValue))

                newDict = data[name]
                newDict['first_disparity'] = coinMaspValue[0]['first_disparity']
                newDict['second_disparity'] = coinMaspValue[0]['second_disparity']

                Masp_dict.append({name:newDict})

            if coin.coin_name in Disparity_list:
                name = coin.coin_name[:-4]
                coinDisparityValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, DisparityValue))
                newDict = data[name]
                newDict['disparity'] = coinDisparityValue[0]['disparity']
                Disparity_dict.append({name:newDict})

            if coin.coin_name in Trend_list:
                name = coin.coin_name[:-4]
                coinTrendValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, TrendValue))
                newDict = data[name]
                newDict['first_value'] = coinTrendValue[0]['first_value']
                newDict['last_value'] = coinTrendValue[0]['last_value']
                Trend_dict.append({name:newDict})

            if coin.coin_name in Macd_list:
                name = coin.coin_name[:-4]
                coinMacdValue = list(filter(lambda item : item['coin_name'] == coin.coin_name, MacdValue))

                newDict = data[name]
                newDict['macd_short'] = coinMacdValue[0]['macd_short']
                newDict['macd_long'] = coinMacdValue[0]['macd_long']
                newDict['macd'] = coinMacdValue[0]['macd']
                newDict['macd_signal'] = coinMacdValue[0]['macd_signal']
                Macd_dict.append({name:newDict})

            if coin.coin_name in coin_name_list:
                name = coin.coin_name[:-4]

                recommend_dict.append({name:data[name]})

        now2 = datetime.datetime.now()
        db.close()
        insert_list = []

        if len(recommend_dict) != 0:
            for coin in recommend_dict:
                coinKey = list(coin.keys())
                coinValue = list(coin.values())
                insert_list.append({'name':coinKey[0], 'price':coinValue[0]['closing_price']})
                coinValue[0]['closing_price']
                coinKey[0]

        print('spend time ::::::: ', now2 - now1)
        return {'recommends': recommend_dict, 'Price':Price_dict, 'TransactioAmount':TA_dict, 'Masp':Masp_dict, 'Trend': Trend_dict, 'Disparity':Disparity_dict, 'MACD': Macd_dict}