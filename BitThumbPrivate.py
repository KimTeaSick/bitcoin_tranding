from dotenv import load_dotenv
from pybithumb import Bithumb
from datetime import datetime
from pandas import DataFrame
from dbConnection import *
from parameter import *
from multiprocessing import Pool
import multiprocessing as mp
from lib import *
from sql import *
from dbConnection import MySql
import pandas as pd
import numpy as np
import websockets
import schedule
import requests
import time
import json
import recommend
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
from returnValue import changer
import subprocess


load_dotenv()
secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"

h = "24h"
url = f"https://api.bithumb.com/public/candlestick/BTC_KRW/{h}"
headers = {"accept": "application/json"}

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()


class BitThumbPrivate():
    def __init__(self):
        self.bithumb = Bithumb(connenctKey, secretKey)
        self.coinList = list(self.getBitCoinList('ALL')['data'].keys())[0:-1]
        self.recommandCoinList = []
        # self.bitLib = bitLib()
        self.mysql = MySql()

    async def getMyPossessionCoinList(self):
        myCoinList = await self.mysql.Select(getMyCoinListSql)
        return myCoinList

    def callGetTradingFee(self):  # 수수료 구하기
        print(self.bithumb.get_trading_fee("BTC"))

    def getBitCoinList(self, coin):  # 코인 리스트, 코인 정보 가져오기
        url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
        headers = {"accept": "application/json"}
        response = json.loads(requests.get(url, headers=headers).text)
        return response

    def getCandleStick(self, item):  # 차트 데이터
        dataList = []
        url = f"https://api.bithumb.com/public/candlestick/{item.id}_KRW/{item.term}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response = json.loads(response)
        if type(response) == dict:
            response = response['data']
            df = DataFrame(response, columns=[
                           'Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
            for i in range(0, len(df)):
                data = df.iloc[i]
                data.Date = int(data.Date)
                data.Open = float(data.Open)
                data.Close = float(data.Close)
                data.High = float(data.High)
                data.Low = float(data.Low)
                data.Volume = float(data.Volume)
                dataList.append(data)
            _d = tuple(dataList)
            return _d[-121:-1]

    def calndel_for_search(self, item):
        coin = item["id"]
        term = item["term"]
        url = f"https://api.bithumb.com/public/candlestick/{coin}_KRW/{term}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response = json.loads(response)
        return response

    def getCoinOrderBook(self, coin):  # 코인 거래 내역
        orderBook = self.bithumb.get_orderbook(coin)
        return orderBook

    def checkAccount(self):  # 보유 예수금 목록
        try:
            response = self.bithumb.get_balance('BTC')
            KRW = response[2]
            return KRW
        except Exception as e:
            print("checkAccount Error :::: ", e)
            return 444

    def setBuyCondition(self):  # 매수 조건
        url = f"https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}
        response = json.loads(requests.get(url, headers=headers).text)
        allData = list(dict.items(response['data']))[0: -1]
        matchList = []
        for item in allData:
            if float(item[1]["acc_trade_value_24H"]) >= 1000000000.8963:
                if float(item[1]["fluctate_rate_24H"]) >= 3.00:
                    matchList.append(item)
        for item in matchList:
            print(item[0])
        return matchList

    def getMyCoinList(self):  # 현재 보유 코인 종류
        coinList = self.bithumb.get_balance('All')
        coinList = coinList['data']
        coinTotalList = dict.items(coinList)
        totalList = []
        myCoinList = []
        for item in coinTotalList:
            if ('total_' in str(item[0])):
                totalList.append(item)
        for item in totalList:
            if (float(item[1]) >= 0.0001):
                if item[0] != 'total_krw':
                    if item[0] != 'total_bm':
                        myCoinList.append(item)
        return myCoinList

    def getTransactionHistory(self, target):  # 거래내역
        print(self.bithumb.get_transaction_history(target))

    def getOrderCompleted(self):
        print(self.bithumb.get_order_completed())

    def getBuyPrice(self, coin):
        buyPrice = self.bithumb.get_orderbook(coin)['bids'][1]['price']
        return buyPrice

    def buyQuantity(self, buyPrice):
        buy_quantity = self.checkAccount() * 0.9970 / buyPrice  # 수수료 0.25% 계산
        buy_quantity = float("{:.4f}".format(buy_quantity))  # 소수점 4자리 수 버림
        return buy_quantity

    def bulkSale(self):
        coinList = self.getMyCoinList()
        for coin in coinList:
            coinName = (str(coin[0]).replace('total_', ""))
            if (coinName != 'krw'):
                coinName = coinName.upper()
                self.sell(coinName, float(coin[1]))

    def coinNameList(self):
        coinNames = self.bithumb.get_tickers()
        for index in range(len(coinNames)):
            coinNames[index] += "_KRW"
        return coinNames

    def myProperty(self):
        coinList = self.getMyCoinList()
        list = []
        money = 0
        for i in coinList:
            coinInfo = self.getBitCoinList(str(i[0]).replace('total_', ""))
            if int(coinInfo['status']) == 5500:
                continue
            coinValue = float(
                coinInfo['data']['closing_price']) * round(float(i[1]), 4)
            list.append(coinValue)
        for index in range(len(list)):
            money += list[index]
        account = self.checkAccount()
        money += account
        return money, account

# 거래 내역 조회 및 검색 기능
    # async def getOrderList(self, page):
    #     count = "14"
    #     if (page == 1):
    #         prev = "0"
    #     else:
    #         prev = str((int(page) - 1) * 14)
    #     selectData = await self.mysql.Select(orderListSql(count, prev))
    #     orderList = []
    #     for data in selectData:
    #         orderList.append(changer.ORDER_LIST_CHANGER(data))
    #     return orderList

    # def getDateOrderList(self, date, page):
    #     count = "14"
    #     if (page == 1):
    #         prev = "0"
    #     else:
    #         prev = str((int(page) - 1) * 14)
    #     selectData = self.mysql.Select(
    #         dateOrderListSql(count, prev, date[0], date[1]))
    #     orderList = []
    #     for data in selectData:
    #         orderDesc = (data[2], data[1], data[3], 'KRW')
    #         orderList.append(
    #             self.bithumb.get_order_completed(orderDesc)['data'])
    #     return orderList

# Dash Page
    def getDisparity(self, coin, disparity, trends):
        flag = True
        url = f"https://api.bithumb.com/public/candlestick/"+coin[0]+"_KRW/6h"
        headers = {"accept": "application/json"}
        data = json.loads(requests.get(url, headers=headers).text)['data']
        df = pd.DataFrame(
            data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
        AR = tuple(df['Close'].rolling(window=5).mean().fillna('undefined'))
        AR_BASE = AR[-10: -1]
        BASE = df['Close'].values.tolist()
        for term in range(0, int(trends)):
            if term == 0:
                separation = (float(
                    BASE[len(BASE) - (term + 1)]) / float(AR_BASE[len(AR_BASE) - (term + 1)])) * 100
                if separation < int(disparity):
                    return ''
            result = float(BASE[len(BASE) - (term + 1)]) - \
                float(AR_BASE[len(AR_BASE) - (term + 1)])
            if result < 0:
                flag = False
                return ''
        if flag == True:
            self.recommandCoinList.append({"coin": {"coin": coin[0], "data": self.getBitCoinList(
                coin[0])["data"]}, "separation": separation})

    async def test(self, coinList, first_disparity, trends):
        for coin in coinList:
            self.getDisparity(coin, first_disparity, trends)

    async def getRecommendCoin(self, item):
        useOptionList = []
        options = []
        mMax = 0
        hMax = 0
        # 사용 옵션 확인 및 변환
        for i in item:
            print(i[0])
            # print("i :::::::::::::::::::: ", i)
            if i[1]['flag'] != 0:
                useOptionList.append(i[0])
                if i[0] == 'Price':
                    if int(i[1]['high_price']) == 0:
                        print('high_price', i[1]['high_price'])
                        continue
                    if 5 > mMax:
                        mMax = 5
                    options.append(
                        {'option': 'Price', 'low_price': i[1]['low_price'], 'high_price': i[1]['high_price']})

                if i[0] == 'TransactionAmount':
                    if int(i[1]['high_transaction_amount']) == 0:
                        print('high_transaction_amount',
                              i[1]['high_transaction_amount'])
                        continue
                    if i[1]['chart_term'][-1] == 'm' and int(i[1]['chart_term'][:-1]) > mMax:
                        mMax = int(i[1]['chart_term'][:-1])
                    if i[1]['chart_term'][-1] == 'h' and int(i[1]['chart_term'][:-1]) > hMax:
                        hMax = int(i[1]['chart_term'][:-1])

                    options.append({'option': 'TransactionAmount', 'chart_term': i[1]['chart_term'], 'low_transaction_amount': i[
                                   1]['low_transaction_amount'], 'high_transaction_amount': i[1]['high_transaction_amount']})

                if i[0] == 'MASP':
                    if int(i[1]['first_disparity']) == 0 or int(i[1]['second_disparity']) == 0:
                        print('first_disparity: ', i[1]['first_disparity'],
                              'second_disparity: ', i[1]['second_disparity'])
                        continue

                    if i[1]['chart_term'][-1] == 'm' and int(i[1]['first_disparity']) * int(i[1]['chart_term'][:-1]) > mMax:
                        mMax = int(i[1]['first_disparity']) * \
                            int(i[1]['chart_term'][:-1])
                    if i[1]['chart_term'][-1] == 'm' and int(i[1]['second_disparity']) * int(i[1]['chart_term'][:-1]) > mMax:
                        mMax = int(i[1]['second_disparity']) * \
                            int(i[1]['chart_term'][:-1])

                    if i[1]['chart_term'][-1] == 'h' and (int(i[1]['first_disparity']) * int(i[1]['chart_term'][:-1])) > hMax:
                        hMax = (int(i[1]['first_disparity'])
                                * int(i[1]['chart_term'][:-1]))
                    if i[1]['chart_term'][-1] == 'h' and (int(i[1]['second_disparity']) * int(i[1]['chart_term'][:-1])) > hMax:
                        hMax = (int(i[1]['second_disparity'])
                                * int(i[1]['chart_term'][:-1]))

                    options.append({'option': 'MASP', 'chart_term': i[1]['chart_term'], 'first_disparity': i[1]
                                   ['first_disparity'], 'second_disparity': i[1]['second_disparity'], 'comparison': i[1]['comparison']})

                if i[0] == 'Disparity':
                    if int(i[1]['disparity_term']) == 0:
                        print('disparity_term:', i[1]['disparity_term'])
                        continue

                    if i[1]['chart_term'][-1] == 'm':
                        if (int(i[1]['disparity_term']) * int(i[1]['chart_term'][:-1])) > mMax:
                            mMax = int(i[1]['disparity_term']) * \
                                int(i[1]['chart_term'][:-1])

                    if i[1]['chart_term'][-1] == 'h':
                        if (int(i[1]['disparity_term']) * int(i[1]['chart_term'][:-1])) > hMax:
                            hMax = (int(i[1]['disparity_term'])
                                    * int(i[1]['chart_term'][:-1]))

                    options.append({'option': 'Disparity', 'chart_term': i[1]['chart_term'], 'disparity_term': i[1]['disparity_term'], 'low_disparity': int(
                        i[1]['low_disparity']), 'high_disparity': int(i[1]['high_disparity'])})

                if i[0] == 'Trend':
                    if int(i[1]['trend_term']) == 0 or int(i[1]['MASP']) == 0:
                        print('trend_term:',
                              i[1]['trend_term'], 'MASP:', i[1]['MASP'])
                        continue

                    if i[1]['chart_term'][-1] == 'm' and ((int(i[1]['trend_term']) + 2 + int(i[1]['MASP'])) * int(i[1]['chart_term'][:-1])) > mMax:
                        mMax = (
                            (int(i[1]['trend_term']) + 2 + int(i[1]['MASP'])) * int(i[1]['chart_term'][:-1]))

                    if i[1]['chart_term'][-1] == 'h' and ((int(i[1]['trend_term']) + 2 + int(i[1]['MASP'])) * int(i[1]['chart_term'][:-1])) > hMax:
                        hMax = (
                            (int(i[1]['trend_term']) + 2 + int(i[1]['MASP'])) * int(i[1]['chart_term'][:-1]))

                    options.append({'option': 'Trend', 'chart_term': i[1]['chart_term'], 'trend_term': i[1]['trend_term'],
                                   'trend_type': i[1]['trend_type'], 'trend_reverse': i[1]['trend_reverse'], "MASP": i[1]['MASP']})

                if i[0] == 'MACD':
                    if int(i[1]['short_disparity']) == 0 or int(i[1]['long_disparity']) == 0:
                        print('short_disparity:', i[1]['short_disparity'],
                              'long_disparity:', i[1]['long_disparity'])
                        continue

                    if i[1]['chart_term'][-1] == 'm' and ((int(i[1]['long_disparity']) * 2 + int(i[1]['signal'])) * int(i[1]['chart_term'][:-1])) > mMax:
                        mMax = (int(i[1]['long_disparity']) * 2 +
                                int(i[1]['signal'])) * int(i[1]['chart_term'][:-1])

                    if i[1]['chart_term'][-1] == 'h' and ((int(i[1]['long_disparity']) * 2 + int(i[1]['signal'])) * int(i[1]['chart_term'][:-1])) > hMax:
                        hMax = (int(i[1]['long_disparity']) * 2 +
                                int(i[1]['signal'])) * int(i[1]['chart_term'][:-1])

                    options.append({'option': 'MACD', 'chart_term': i[1]['chart_term'], 'short_disparity': i[1]['short_disparity'],
                                   'long_disparity': i[1]['long_disparity'], 'signal': i[1]['signal'], 'up_down': i[1]['up_down']})

        # 검색 코인 receive
        coins = await recommend.recommendCoin(options, mMax, hMax)

        if coins == 444:
            return coins

        return {"coins": coins, "optionList": useOptionList}

    async def possessoionCoinInfo(self):
        try:
            possessionCoin = await self.mysql.Select(getMyCoinListSql)
            time.sleep(1)
            if len(possessionCoin) == 0:
                return 203
            else:
                returnList = []
                for coin in possessionCoin:
                    coinInfo = self.getBitCoinList(coin[0])['data']
                    coinValue = float(coinInfo['closing_price'])
                    returnList.append(
                        changer.POSSESSION_COIN_LIST(coin, coinValue))
                print("returnListreturnList", returnList)
                return returnList
        except Exception as e:
            print("possessoionCoinInfo Error :::: ", e)
            return 333

# Setting Page

    async def getSearchOptionList(self):
        value = await self.mysql.Select(selectSearchOptionSql)
        optionList = []
        for data in value:
            optionList.append({
                "idx": data[0],
                "name": data[1],
                "first_disparity": data[2],
                "second_disparity": data[3],
                "trends": data[4],
                "trends_idx": data[5],
                "avg_volume": data[6],
                "transaction_amount": data[7],
                "price": data[8]})
        print(optionList)
        return optionList

    def insertSearchOption(self, item):
        self.mysql.Insert(insertSearchOptionSql, [
            item.name,
            item.first_disparity,
            item.second_disparity,
            item.trends_idx,
            item.trends,
            item.avg_volume,
            item.transaction_amount,
            item.price
        ])

    async def updateSearchOption(self, item):
        await self.mysql.Update(updateSearchOptionSql, [
            item.name,
            item.first_disparity,
            item.second_disparity,
            item.trends_idx,
            item.trends,
            item.avg_volume,
            item.transaction_amount,
            item.price,
            item.idx
        ])

# Auto But and Selling
    async def autoTrading(self):
        uri = "wss://pubwss.bithumb.com/pub/ws"
        # coinNames = self.coinNameList()
        possessionCoin = self.mysql.Select(getMyCoinListSql)
        coinNames = []
        for i in possessionCoin:
            # coinName = str(i[0]).replace('total_',"")
            coinNames.append(i[0].upper()+"_KRW")

        async with websockets.connect(uri, ping_interval=None) as websocket:
            subscribe_fmt = {
                "type": "ticker",
                "symbols": coinNames,
                "tickTypes": ["30M"]
            }
            subscribe_data = json.dumps(subscribe_fmt)
            await websocket.send(subscribe_data)
            while True:
                schedule.run_pending()
                data = await websocket.recv()
                data = json.loads(data)
                data = data.get('content')
                if type(data) == dict:
                    print(data['symbol'], data['closePrice'])
                    for possessionCoinInfo in possessionCoin:
                        if data['symbol'] == possessionCoinInfo[0]+"_KRW":
                            # 부호 반대가 정상
                            if (float(data['closePrice']) - float(possessionCoinInfo[2])) / 100 > 7:
                                print("plus", possessionCoinInfo)
                                self.sell(possessionCoinInfo[0], float(
                                    possessionCoinInfo[1]))
                                await self.autoTrading()
                            elif (float(data['closePrice']) - float(possessionCoinInfo[2])) / 100 < -3:
                                print("minus", possessionCoinInfo)
                                self.sell(possessionCoinInfo[0], float(
                                    possessionCoinInfo[1]))
                                await self.autoTrading()

    async def buy(self, coin, price, unit):  # 매수
        print(coin, price, unit, '333333333333333333333333333333333')
        buyLog = self.bithumb.buy_limit_order(
            coin, price, unit)  # params 1: 종목, 2: 가격, 3: 갯수
        time.sleep(0.1)
        print(buyLog)
        returnLog = list(buyLog)

        return returnLog

    '''  
  async def buy(self, coin, unit): #매수
    buyLog = self.bithumb.buy_market_order(coin, unit) #params 1: 종목, 2: 갯수
    time.sleep(0.1)
    print(buyLog)
    if(type(buyLog) == tuple):
      print(1)
      detailLog = self.bithumb.get_order_completed(buyLog)['data']
      print("detailLog",detailLog)
      if len(detailLog['contract']) > 0:
        self.mysql.Insert(insertTradingLog, [
          buyLog[0],
          buyLog[1],
          buyLog[2],
          buyLog[3],
          detailLog['order_qty'],
          detailLog['contract'][0]['price'],
          detailLog['contract'][0]['fee'],
          detailLog['contract'][0]['total'],
        ])
        myCoinList = await self.getMyPossessionCoinList()
        print(myCoinList)
        if len(myCoinList) == 0:
          self.mysql.Insert(insertPossessionCoin,[
            buyLog[1],
            detailLog['order_qty'],
            detailLog['contract'][0]['price'],
            detailLog['contract'][0]['total'],
            detailLog['contract'][0]['fee']
          ])
        for coin in myCoinList:
          print(coin)
          print("detailLog",detailLog)
          if coin[0] == buyLog[1]:
            print('Yes!!!')
            self.mysql.Insert(buyUpdatePossessionCoin,[
            float(detailLog['order_qty']) + float(coin[1]),
            (float(detailLog['contract'][0]['price']) + float(coin[2]) ) / 2,
            float(detailLog['contract'][0]['total']) + float(coin[3]),
            float(detailLog['contract'][0]['fee']) + float(coin[4]),
            buyLog[1],
          ])
            break
          else:
            print('NO!!!')
            self.mysql.Insert(insertPossessionCoin,[
              buyLog[1],
              detailLog['order_qty'],
              detailLog['contract'][0]['price'],
              detailLog['contract'][0]['total'],
              detailLog['contract'][0]['fee']
            ])
            break
      return 200
    else:
      return 404'''

    async def sell(self, coin, unit):  # 매도
        sellLog = self.bithumb.sell_market_order(
            coin, unit)  # params 1: 종목, 2: 갯수
        time.sleep(0.1)
        if (type(sellLog) == tuple):
            detailLog = self.bithumb.get_order_completed(sellLog)['data']
            if len(detailLog['contract']) > 0:
                self.mysql.Insert(insertTradingLog, [
                    sellLog[0],
                    sellLog[1],
                    sellLog[2],
                    sellLog[3],
                    detailLog['order_qty'],
                    detailLog['contract'][0]['price'],
                    detailLog['contract'][0]['fee'],
                    detailLog['contract'][0]['total'],
                ])
                myCoinList = await self.getMyPossessionCoinList()
                print('Start !!!')
                for coin in myCoinList:
                    print("123123", float(coin[1]) -
                          float(detailLog['order_qty']))
                    print("123123", float(
                        coin[1]) - float(detailLog['order_qty']) < 0.00)
                    if (float(coin[1]) - float(detailLog['order_qty'])) <= 0.00:
                        print('Yes!!!')
                        self.mysql.Delete(deletePossessionCoin, [coin[0]])
                        break
                    else:
                        print('NO!!!')
                        self.mysql.Update(sellUpdatePossessionCoin, [
                            float(coin[1]) - float(detailLog['order_qty']),
                            float(coin[3]) -
                            float(detailLog['contract'][0]['total']),
                            sellLog[1],
                        ])
                        break
                return 200
            else:
                return 404

    async def insertOption(self, item):
        try:
            print(item)
            opName = ''
            search_option = models.searchOption()
            price_option = models.PriceOption()
            transactionAmount_option = models.TransactionAmountOption()
            MASP_option = models.MASPOption()
            disparity_option = models.DisparityOption()
            trend_option = models.TrendOption()
            MACD_option = models.MACDOption()

            for i in item:
                if i[0] == 'Name':
                    opName = i[1]

                if i[0] == 'Price':
                    price_option.flag = i[1]['flag']
                    price_option.low_price = i[1]['low_price']
                    price_option.high_price = i[1]['high_price']
                    price_option.name = opName
                    db.add(price_option)

                if i[0] == 'TransactionAmount':
                    transactionAmount_option.flag = i[1]['flag']
                    transactionAmount_option.chart_term = i[1]['chart_term']
                    transactionAmount_option.low_transaction_amount = i[1]['low_transaction_amount']
                    transactionAmount_option.high_transaction_amount = i[1]['high_transaction_amount']
                    transactionAmount_option.name = opName
                    db.add(transactionAmount_option)

                if i[0] == 'MASP':
                    MASP_option.flag = i[1]['flag']
                    MASP_option.chart_term = i[1]['chart_term']
                    MASP_option.first_disparity = i[1]['first_disparity']
                    MASP_option.comparison = i[1]['comparison']
                    MASP_option.second_disparity = i[1]['second_disparity']
                    MASP_option.name = opName
                    db.add(MASP_option)

                if i[0] == 'Disparity':
                    disparity_option.flag = i[1]['flag']
                    disparity_option.chart_term = i[1]['chart_term']
                    disparity_option.disparity_term = i[1]['disparity_term']
                    disparity_option.low_disparity = i[1]['low_disparity']
                    disparity_option.high_disparity = i[1]['high_disparity']
                    disparity_option.name = opName
                    db.add(disparity_option)

                if i[0] == 'Trend':
                    trend_option.flag = i[1]['flag']
                    trend_option.chart_term = i[1]['chart_term']
                    trend_option.MASP = i[1]['MASP']
                    trend_option.trend_term = i[1]['trend_term']
                    trend_option.trend_type = i[1]['trend_type']
                    trend_option.trend_reverse = i[1]['trend_reverse']
                    trend_option.name = opName
                    db.add(trend_option)

                if i[0] == 'MACD':
                    MACD_option.flag = i[1]['flag']
                    MACD_option.chart_term = i[1]['chart_term']
                    MACD_option.short_disparity = i[1]['short_disparity']
                    MACD_option.long_disparity = i[1]['long_disparity']
                    MACD_option.up_down = i[1]['up_down']
                    MACD_option.signal = i[1]['signal']
                    MACD_option.name = opName
                    db.add(MACD_option)

            search_option.name = opName
            search_option.Price = opName
            search_option.Transaction_amount = opName
            search_option.MASP = opName
            search_option.Disparity = opName
            search_option.Trend = opName
            search_option.MACD = opName
            search_option.Create_date = datetime.datetime.now()
            search_option.used = 0

            db.add(search_option)

            try:
                db.commit()
                return 'Insert sucess'

            except Exception as e:
                db.rollback()
                print("db.rollback()", e)
                return 444

        except Exception as e:
            print(e)
            return 444

    async def optionList(self):
        try:
            optionL = db.query(models.searchOption).all()
            options = []

            for option in optionL:
                if option.Update_date == None:
                    option.Update_date = "-"
                else:
                    option.Update_date = option.Update_date[0:19]
                options.append(
                    {'Name': option.name, 'Create_date': option.Create_date[0:19], 'Update_date': option.Update_date, 'used': option.used})
            return options
        except Exception as e:
            print("optionList Error :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def optionDetail(self, item):
        try:
            print(item)
            now1 = datetime.datetime.now()

            optionL = db.query(models.searchOption).filter(
                models.searchOption.name == item.option).first()

            pri = db.query(models.PriceOption).filter(
                models.PriceOption.name == optionL.Price).first()
            tra = db.query(models.TransactionAmountOption).filter(
                models.TransactionAmountOption.name == optionL.Transaction_amount).first()
            mas = db.query(models.MASPOption).filter(
                models.MASPOption.name == optionL.MASP).first()
            dis = db.query(models.DisparityOption).filter(
                models.DisparityOption.name == optionL.Disparity).first()
            trd = db.query(models.TrendOption).filter(
                models.TrendOption.name == optionL.Trend).first()
            mac = db.query(models.MACDOption).filter(
                models.MACDOption.name == optionL.MACD).first()

            now2 = datetime.datetime.now()
            print(now2-now1)

            return {optionL.name: {'Price': {"low_price": pri.low_price, "high_price": pri.high_price, "flag": pri.flag},
                                   "TransactionAmount": {"chart_term": tra.chart_term, "low_transaction_amount": tra.low_transaction_amount, "high_transaction_amount": tra.high_transaction_amount, "flag": tra.flag},
                                   "MASP": {"chart_term": mas.chart_term, "first_disparity": mas.first_disparity, "comparison": mas.comparison, "second_disparity": mas.second_disparity, "flag": mas.flag},
                                   "Trend": {"chart_term": trd.chart_term, "MASP": trd.MASP, "trend_term": trd.trend_term, "trend_type": trd.trend_type, "trend_reverse": trd.trend_reverse, "flag": trd.flag},
                                   "Disparity": {"chart_term": dis.chart_term, "disparity_term": dis.disparity_term, "low_disparity": dis.low_disparity, "high_disparity": dis.high_disparity, "flag": dis.flag},
                                   "MACD": {"chart_term": mac.chart_term, "short_disparity": mac.short_disparity, "long_disparity": mac.long_disparity, "up_down": mac.up_down, "flag": mac.flag, "signal": mac.signal}}}
        except Exception as e:
            print("optionList Error :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def updateOption(self, item):
        opName = ''
        for i in item:
            if i[0] == 'Name':
                opName = i[1]

            if i[0] == 'Price':
                low_price = i[1]['low_price']
                high_price = i[1]['high_price']
                PriFlag = i[1]['flag']

            if i[0] == 'TransactionAmount':
                low_transaction_amount = i[1]['low_transaction_amount']
                high_transaction_amount = i[1]['high_transaction_amount']
                Trachart_term = i[1]['chart_term']
                TraFlag = i[1]['flag']

            if i[0] == 'MASP':
                Schart_term = i[1]['chart_term']
                first_disparity = i[1]['first_disparity']
                comparison = i[1]['comparison']
                second_disparity = i[1]['second_disparity']
                MasFlag = i[1]['flag']

            if i[0] == 'Disparity':
                Dchart_term = i[1]['chart_term']
                disparity_term = i[1]['disparity_term']
                low_disparity = i[1]['low_disparity']
                high_disparity = i[1]['high_disparity']
                DisFlag = i[1]['flag']

            if i[0] == 'Trend':
                Tchart_term = i[1]['chart_term']
                MASP = i[1]['MASP']
                trend_term = i[1]['trend_term']
                trend_type = i[1]['trend_type']
                trend_reverse = i[1]['trend_reverse']
                TrdFlag = i[1]['flag']

            if i[0] == 'MACD':
                Cchart_term = i[1]['chart_term']
                short_disparity = i[1]['short_disparity']
                long_disparity = i[1]['long_disparity']
                signal = i[1]['signal']
                up_down = i[1]['up_down']
                MacFlag = i[1]['flag']

        optionL = db.query(models.searchOption).filter(
            models.searchOption.name == opName).first()

        pri = db.query(models.PriceOption).filter(
            models.PriceOption.name == optionL.Price).first()
        tra = db.query(models.TransactionAmountOption).filter(
            models.TransactionAmountOption.name == optionL.Transaction_amount).first()
        mas = db.query(models.MASPOption).filter(
            models.MASPOption.name == optionL.MASP).first()
        dis = db.query(models.DisparityOption).filter(
            models.DisparityOption.name == optionL.Disparity).first()
        trd = db.query(models.TrendOption).filter(
            models.TrendOption.name == optionL.Trend).first()
        mac = db.query(models.MACDOption).filter(
            models.MACDOption.name == optionL.MACD).first()

        pri.low_price = low_price
        pri.high_price = high_price
        pri.flag = PriFlag

        tra.chart_term = Trachart_term
        tra.low_transaction_amount = low_transaction_amount
        tra.high_transaction_amount = high_transaction_amount
        tra.flag = TraFlag

        mas.chart_term = Schart_term
        mas.first_disparity = first_disparity
        mas.comparison = comparison
        mas.second_disparity = second_disparity
        mas.flag = MasFlag

        dis.chart_term = Dchart_term
        dis.disparity_term = disparity_term
        dis.low_disparity = low_disparity
        dis.high_disparity = high_disparity
        dis.flag = DisFlag

        trd.chart_term = Tchart_term
        trd.MASP = MASP
        trd.trend_term = trend_term
        trd.trend_type = trend_type
        trd.trend_reverse = trend_reverse
        trd.flag = TrdFlag

        mac.chart_term = Cchart_term
        mac.short_disparity = short_disparity
        mac.long_disparity = long_disparity
        mac.signal = signal
        mac.up_down = up_down
        mac.flag = MacFlag

        optionL.Update_date = datetime.datetime.now()

        try:
            db.commit()
            print('commit')
        except:
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            print('rollback')

        return 'Insert sucess'

    async def deleteOption(self, item):
        try:
            optionL = db.query(models.searchOption).filter(
                models.searchOption.name == item.option).first()

            db.query(models.PriceOption).filter(
                models.PriceOption.name == item.option).delete()
            db.query(models.TransactionAmountOption).filter(
                models.TransactionAmountOption.name == item.option).delete()
            db.query(models.MASPOption).filter(
                models.MASPOption.name == item.option).delete()
            db.query(models.DisparityOption).filter(
                models.DisparityOption.name == item.option).delete()
            db.query(models.TrendOption).filter(
                models.TrendOption.name == item.option).delete()
            db.query(models.MACDOption).filter(
                models.MACDOption.name == item.option).delete()

            db.query(models.searchOption).filter(
                models.searchOption.name == item.option).delete()

            try:
                db.commit()
            except Exception as e:
                print(e)
                self.mysql.Insert(insertLog, [e])
                db.rollback()

            return 'delete sucess'

        except Exception as e:
            print(e)

    async def useOption(self, item):
        try:
            print("useOption :::::", item)
            useOption = db.query(models.searchOption).filter(
                models.searchOption.name == item.option).first()
            print("useOption :::::", useOption.name)
            optionL = db.query(models.searchOption).filter(
                models.searchOption.used == 1).all()
            print("optionL :::::", optionL)

            for option in optionL:
                option.used = 0

            useOption.used = 1
            useOption.Update_date = datetime.datetime.now()
            db.commit()
            print("success :::::")
            return 200
        except Exception as e:
            print("fail :::::", e)
            db.rollback()
            return 444

# ===============================================================================================================trading option

    async def insertTradingOPtion(self, item):
        try:
            print(item.name)
            trading_option = models.tradingOption()
            trading_account_option = models.tradingAccountOtion()
            trading_buy_option = models.tradingBuyOption()
            trading_sell_option = models.tradingSellOption()

            for i in item:
                print(item.name, i[0])
                if i[0] == 'account':
                    trading_account_option.name = item.name
                    trading_account_option.price_count = i[1]['price_count']
                    trading_account_option.loss_cut_under_percent = i[1]['loss_cut_under_percent']
                    trading_account_option.loss = i[1]['loss']
                    trading_account_option.loss_cut_under_call_price_sell_all = i[
                        1]['loss_cut_under_call_price_sell_all']
                    trading_account_option.loss_cut_under_coin_specific_percent = opName = i[
                        1]['loss_cut_under_coin_specific_percent']
                    trading_account_option.loss_cut_under_call_price_specific_coin = i[
                        1]['loss_cut_under_call_price_specific_coin']
                    trading_account_option.loss_cut_over_percent = i[1]['loss_cut_over_percent']
                    trading_account_option.gain = i[1]['gain']
                    trading_account_option.loss_cut_over_call_price_sell_all = i[
                        1]['loss_cut_over_call_price_sell_all']
                    trading_account_option.loss_cut_over_coin_specific_percent = i[
                        1]['loss_cut_over_coin_specific_percent']
                    trading_account_option.loss_cut_over_call_price_specific_coin = i[
                        1]['loss_cut_over_call_price_specific_coin']
                    trading_account_option.buy_cancle_time = i[1]['buy_cancle_time']
                    trading_account_option.sell_cancle_time = i[1]['sell_cancle_time']

                    db.add(trading_account_option)

                if i[0] == 'buy':
                    trading_buy_option.name = item.name
                    trading_buy_option.percent_to_buy_method = i[1]['percent_to_buy_method']
                    trading_buy_option.price_to_buy_method = i[1]['price_to_buy_method']
                    trading_buy_option.callmoney_to_buy_method = i[1]['callmoney_to_buy_method']
                    trading_buy_option.checkbox = i[1]['checkbox']
                    db.add(trading_buy_option)

                if i[0] == 'sell':
                    trading_sell_option.name = item.name
                    trading_sell_option.upper_percent_to_price_condition = i[
                        1]['upper_percent_to_price_condition']
                    trading_sell_option.down_percent_to_price_condition = i[
                        1]['down_percent_to_price_condition']
                    trading_sell_option.disparity_for_upper_case = i[1]['disparity_for_upper_case']
                    trading_sell_option.upper_percent_to_disparity_condition = i[
                        1]['upper_percent_to_disparity_condition']
                    trading_sell_option.disparity_for_down_case = i[1]['disparity_for_down_case']
                    trading_sell_option.down_percent_to_disparity_condition = i[
                        1]['down_percent_to_disparity_condition']
                    trading_sell_option.call_money_to_sell_method = i[1]['call_money_to_sell_method']
                    trading_sell_option.percent_to_split_sell = i[1]['percent_to_split_sell']
                    trading_sell_option.shot_MACD_value = i[1]['shot_MACD_value']
                    trading_sell_option.long_MACD_value = i[1]['long_MACD_value']
                    trading_sell_option.MACD_signal_value = i[1]['MACD_signal_value']

                    trading_sell_option.trailing_start_percent = i[1]['trailing_start_percent']
                    trading_sell_option.trailing_stop_percent = i[1]['trailing_stop_percent']
                    trading_sell_option.trailing_order_call_price = i[1]['trailing_order_call_price']

                    db.add(trading_sell_option)

            trading_option.name = item.name
            trading_option.insert_time = datetime.datetime.now()
            trading_option.update_time = "-"
            trading_option.used = 0
            print(item.name)

            db.add(trading_option)

            try:
                db.commit()
                return 'Insert sucess'

            except Exception as e:
                db.rollback()
                print("db.rollback()", e)
                self.mysql.Insert(insertLog, [e])
                return 444

        except Exception as e:
            print(e)
            return 444

    async def tradingOptionList(self):
        try:
            optionL = db.query(models.tradingOption).all()
            options = []

            for option in optionL:
                options.append(
                    {'Name': option.name, 'Create_date': option.insert_time[:19], 'Update_date': option.update_time[:19], 'used': option.used})
                print(options)

            return options
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def tradingOptionDetail(self, item):
        try:
            print(item)
            now1 = datetime.datetime.now()

            optionL = db.query(models.tradingOption).filter(
                models.tradingOption.name == item.name).first()

            accountL = db.query(models.tradingAccountOtion).filter(
                models.tradingAccountOtion.name == item.name).first()
            buyL = db.query(models.tradingBuyOption).filter(
                models.tradingBuyOption.name == item.name).first()
            sellL = db.query(models.tradingSellOption).filter(
                models.tradingSellOption.name == item.name).first()

            now2 = datetime.datetime.now()
            print(now2-now1)

            return {optionL.name: {'account': {"price_count": accountL.price_count, "loss_cut_under_percent": accountL.loss_cut_under_percent, "loss_cut_under_call_price_sell_all": accountL.loss_cut_under_call_price_sell_all, "loss_cut_under_coin_specific_percent": accountL.loss_cut_under_coin_specific_percent, "loss_cut_under_call_price_specific_coin": accountL.loss_cut_under_call_price_specific_coin, "loss_cut_over_percent": accountL.loss_cut_over_percent, "loss_cut_over_call_price_sell_all": accountL.loss_cut_over_call_price_sell_all, "loss_cut_over_coin_specific_percent": accountL.loss_cut_over_coin_specific_percent, "loss_cut_over_call_price_specific_coin": accountL.loss_cut_over_call_price_specific_coin, "buy_cancle_time": accountL.buy_cancle_time, "sell_cancle_time": accountL.sell_cancle_time, "loss": accountL.loss, "gain": accountL.gain},
                                   "buy": {"percent_to_buy_method": buyL.percent_to_buy_method, "price_to_buy_method": buyL.price_to_buy_method, "callmoney_to_buy_method": buyL.callmoney_to_buy_method, "checkbox": buyL.checkbox},
                                   "sell": {"upper_percent_to_price_condition": sellL.upper_percent_to_price_condition, "down_percent_to_price_condition": sellL.down_percent_to_price_condition, "disparity_for_upper_case": sellL.disparity_for_upper_case, "upper_percent_to_disparity_condition": sellL.upper_percent_to_disparity_condition, "disparity_for_down_case": sellL.disparity_for_down_case, "down_percent_to_disparity_condition": sellL.down_percent_to_disparity_condition, "call_money_to_sell_method": sellL.call_money_to_sell_method, "percent_to_split_sell": sellL.percent_to_split_sell, "shot_MACD_value": sellL.shot_MACD_value, "long_MACD_value": sellL.long_MACD_value, "MACD_signal_value": sellL.MACD_signal_value, "trailing_start_percent": sellL.trailing_start_percent, "trailing_stop_percent": sellL.trailing_stop_percent, "trailing_order_call_price": sellL.trailing_order_call_price}
                                   }}
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def updateTradingOption(self, item):
        try:
            print(item.name)

            for i in item:
                if i[0] == 'account':
                    price_count = i[1]['price_count']
                    loss_cut_under_percent = i[1]['loss_cut_under_percent']
                    loss = i[1]['loss']
                    loss_cut_under_call_price_sell_all = i[1]['loss_cut_under_call_price_sell_all']
                    loss_cut_under_coin_specific_percent = opName = i[
                        1]['loss_cut_under_coin_specific_percent']
                    loss_cut_under_call_price_specific_coin = i[1]['loss_cut_under_call_price_specific_coin']
                    loss_cut_over_percent = i[1]['loss_cut_over_percent']
                    gain = i[1]['gain']
                    loss_cut_over_call_price_sell_all = i[1]['loss_cut_over_call_price_sell_all']
                    loss_cut_over_coin_specific_percent = i[1]['loss_cut_over_coin_specific_percent']
                    loss_cut_over_call_price_specific_coin = i[1]['loss_cut_over_call_price_specific_coin']
                    buy_cancle_time = i[1]['buy_cancle_time']
                    sell_cancle_time = i[1]['sell_cancle_time']

                if i[0] == 'buy':
                    percent_to_buy_method = i[1]['percent_to_buy_method']
                    price_to_buy_method = i[1]['price_to_buy_method']
                    callmoney_to_buy_method = i[1]['callmoney_to_buy_method']
                    checkbox = i[1]['checkbox']

                if i[0] == 'sell':
                    upper_percent_to_price_condition = i[1]['upper_percent_to_price_condition']
                    down_percent_to_price_condition = i[1]['down_percent_to_price_condition']
                    disparity_for_upper_case = i[1]['disparity_for_upper_case']
                    upper_percent_to_disparity_condition = i[1]['upper_percent_to_disparity_condition']
                    disparity_for_down_case = i[1]['disparity_for_down_case']
                    down_percent_to_disparity_condition = i[1]['down_percent_to_disparity_condition']
                    call_money_to_sell_method = i[1]['call_money_to_sell_method']
                    percent_to_split_sell = i[1]['percent_to_split_sell']
                    shot_MACD_value = i[1]['shot_MACD_value']
                    long_MACD_value = i[1]['long_MACD_value']
                    MACD_signal_value = i[1]['MACD_signal_value']
                    trailing_start_percent = i[1]['trailing_start_percent']
                    trailing_stop_percent = i[1]['trailing_stop_percent']
                    trailing_order_call_price = i[1]['trailing_order_call_price']

            optionL = db.query(models.tradingOption).filter(
                models.tradingOption.name == item.name).first()

            accountL = db.query(models.tradingAccountOtion).filter(
                models.tradingAccountOtion.name == item.name).first()
            buyL = db.query(models.tradingBuyOption).filter(
                models.tradingBuyOption.name == item.name).first()
            sellL = db.query(models.tradingSellOption).filter(
                models.tradingSellOption.name == item.name).first()

            accountL.price_count = price_count
            accountL.loss_cut_under_percent = loss_cut_under_percent
            accountL.loss = loss
            accountL.loss_cut_under_call_price_sell_all = loss_cut_under_call_price_sell_all
            accountL.loss_cut_under_coin_specific_percent = loss_cut_under_coin_specific_percent
            accountL.loss_cut_under_call_price_specific_coin = loss_cut_under_call_price_specific_coin
            accountL.loss_cut_over_percent = loss_cut_over_percent
            accountL.gain = gain
            accountL.loss_cut_over_call_price_sell_all = loss_cut_over_call_price_sell_all
            accountL.loss_cut_over_coin_specific_percent = loss_cut_over_coin_specific_percent
            accountL.loss_cut_over_call_price_specific_coin = loss_cut_over_call_price_specific_coin
            accountL.buy_cancle_time = buy_cancle_time
            accountL.sell_cancle_time = sell_cancle_time

            buyL.percent_to_buy_method = percent_to_buy_method
            buyL.price_to_buy_method = price_to_buy_method
            buyL.callmoney_to_buy_method = callmoney_to_buy_method
            buyL.checkbox = checkbox

            sellL.upper_percent_to_price_condition = upper_percent_to_price_condition
            sellL.down_percent_to_price_condition = down_percent_to_price_condition
            sellL.disparity_for_upper_case = disparity_for_upper_case
            sellL.upper_percent_to_disparity_condition = upper_percent_to_disparity_condition
            sellL.disparity_for_down_case = disparity_for_down_case
            sellL.down_percent_to_disparity_condition = down_percent_to_disparity_condition
            sellL.call_money_to_sell_method = call_money_to_sell_method
            sellL.percent_to_split_sell = percent_to_split_sell
            sellL.shot_MACD_value = shot_MACD_value
            sellL.long_MACD_value = long_MACD_value
            sellL.MACD_signal_value = MACD_signal_value
            sellL.trailing_start_percent = trailing_start_percent
            sellL.trailing_stop_percent = trailing_stop_percent
            sellL.trailing_order_call_price = trailing_order_call_price

            optionL.update_time = datetime.datetime.now()

            try:
                db.commit()
                print('commit')
            except Exception as e:
                print("tradingOptionListError :::: ", e)
                self.mysql.Insert(insertLog, [e])
                db.rollback()
                return 444

            return 'Insert sucess'
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def deleteTradingOption(self, item):
        try:
            db.query(models.tradingOption).filter(
                models.tradingOption.name == item.name).delete()

            db.query(models.tradingAccountOtion).filter(
                models.tradingAccountOtion.name == item.name).delete()
            db.query(models.tradingBuyOption).filter(
                models.tradingBuyOption.name == item.name).delete()
            db.query(models.tradingSellOption).filter(
                models.tradingSellOption.name == item.name).delete()

            try:
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()

            return 'delete sucess'

        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            db.rollback()
            return 444

    async def useTradingOption(self, item):
        print(item)
        useOption = db.query(models.tradingOption).filter(
            models.tradingOption.name == item.name).first()
        optionL = db.query(models.tradingOption).filter(
            models.tradingOption.used == 1).all()
        for option in optionL:
            option.used = 0
        useOption.used = 1
        useOption.Update_date = datetime.datetime.now()
        try:
            db.commit()
        except:
            db.rollback()

    async def getSearchPriceList(self):
        try:
            returnValue = []
            searchList = await self.mysql.Select(selectSearchPriceList)
            for coin in searchList:
                returnValue.append({'name': coin[1], 'catch_price': coin[2]})
            return returnValue
        except Exception as e:
            print("getSearchPriceList :::: ", e)
            self.mysql.Insert(insertLog, [e])
            return 444

    async def getNowUseCondition(self):
        try:
            searchCondition = await self.mysql.Select(findUseSearchCondition)
            tradingCondition = await self.mysql.Select(findUseTradingCondition)
            searchOption = await self.mysql.Select(useSearchOptionStatus(searchCondition[0][1]))
            tradingOption = await self.mysql.Select(useTradingOptionStatus(tradingCondition[0][0]))
            searchOptionReturnValue = changer.SEARCH_CONDITION(searchOption)
            tradingOptionReturnValue = changer.TRADING_CONDITION(tradingOption)
            return {"searchOption": searchOptionReturnValue, "tradingOption": tradingOptionReturnValue}
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            return 444

    async def getTradingHis(self):
        try:
            returnValue = []
            tradingHis = await self.mysql.Select(getTradingHisSql())

            if (tradingHis != None):
                for his in tradingHis:
                    returnValue.append(changer.TRADING_LIST(his))
            return returnValue
        except:
            return 444

    async def nowAutoStatusCheck(self):
        try:
            status = await self.mysql.Select(autoStatusCheck)
            return {"now_status": status[0][0]}
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            return 444

    async def controlAutoTrading(self, flag):
        try:
            if (flag == 1):
                await self.mysql.Update(updateAutoStatus, [flag, str(datetime.datetime.now().replace())])
                subprocess.run(
                    ['/bin/python3', '/data/4season/bitcoin_trading_back/autoBuy.py'])
            elif (flag == 0):
                orderList = db.query(models.orderCoin).all()
                for order in orderList:
                    Possession = db.query(models.possessionCoin).filter(
                        models.possessionCoin.coin == order.coin).first()
                    if order.status == 1:
                        order_desc = ['bid', order.coin, order.order_id, 'KRW']
                    elif order.status == 3 or order.status == 5:
                        order_desc = ['ask', order.coin, order.order_id, 'KRW']

                    cancel = self.bithumb.cancel_order(order_desc)
                    if cancel == True:
                        if order.status == 1:
                            db.delete(Possession)
                        elif order.status == 3 or order.status == 5:
                            Possession.status = 4

                        db.delete(order)
                        Possession.status = 0
                    try:
                        db.commit()
                    except:
                        db.rollback()

                await self.mysql.Update(updateAutoStatus, [flag, "-"])
            return 200
        except Exception as e:
            print("tradingOptionListError :::: ", e)
            self.mysql.Insert(insertLog, [e])
            return 444

    async def todayAccount(self):
        try:
            dt = str(datetime.datetime.now().replace())
            start_dt = dt[0:10] + " 00:00:00.000000"
            end_dt = dt[0:10] + " 23:59:59.999999"
            total_and_deposit = self.myProperty()
            today_buy_price = await self.mysql.Select(todayBuyPrice(start_dt, end_dt))
            today_sell_price = await self.mysql.Select(todaySellPrice(start_dt, end_dt))
            return changer.TODAY_TRADING_RESULT([today_buy_price, today_sell_price, total_and_deposit[0], total_and_deposit[1]])
        except Exception as e:
            print(e)

    async def nowRate(self):
        try:
            row_yesterday_balance = await self.mysql.Select(get_yesterday_balance)
            yesterday_balance = row_yesterday_balance[0][0]
            print("yesterday_balance :::: ", yesterday_balance)
            now_balance = self.myProperty()[0]
            print("now_balance :::: ", now_balance)
            now_rate = ((round(now_balance)-yesterday_balance) /
                        round(now_balance))*100
            print("now_rate :::: ", round(now_rate, 3))
            return {"rate": round(now_rate, 3), "now_balance": round(now_balance)}
        except Exception as e:
            print(e)

    async def getBithumbCoinList(self):
        try:
            row_coin_list = await self.mysql.Select(get_bithumb_coin_list_sql)
            coin_list = changer.BITHUMB_COIN_LIST(row_coin_list)
            with open('/data/4season/nc_bit_trading/src/variables/coin_list.json', 'w', encoding="utf-8") as make_file:
                json.dump(coin_list, make_file, ensure_ascii=False, indent="\t")
            return coin_list
        except Exception as e:
            print("Error :::: ",e)
            return

    async def getATOrderList(self):
        return_value = []
        raw_data = await self.mysql.Select(getATOrderList)
        if len(raw_data) == 0:
            return return_value
        else:
            for o_list in raw_data:
                return_value.append(changer.ATOrderList(o_list))
        return return_value
