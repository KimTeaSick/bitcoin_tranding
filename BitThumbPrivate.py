from dotenv import load_dotenv
from pybithumb import Bithumb
from datetime import datetime
from pandas import DataFrame
from dbConnection import *
from parameter import *
from multiprocessing import Process
import multiprocessing as mp
from lib import * 
from sql import *
from dbConnection import MySql
import pandas as pd
import numpy as np
import websockets
import requests
import asyncio
import time
import json
import os 

load_dotenv()
secretKey = os.environ.get('SECLET_KEY')
connenctKey = os.environ.get('CONNECT_KEY')

h ="24h"
url = f"https://api.bithumb.com/public/candlestick/BTC_KRW/{h}"
headers = {"accept": "application/json"}

class BitThumbPrivate():
  def __init__(self):
    self.bithumb = Bithumb(connenctKey, secretKey)
    self.coinList = list(self.getBitCoinList('ALL')['data'].keys())[0:-1]
    self.coinNames = []
    self.recommandCoinList = []
    self.possessionCoinList = []
    self.bitLib = bitLib()
    self.mysql = MySql()
    self.myDeposit = 0
    self.myTotalMoney = 0

  async def getMyPossessionCoinList(self):
    myCoinList = await self.mysql.Select(getMyCoinListSql)
    return myCoinList

  def callGetTradingFee(self): # 수수료 구하기
    print(self.bithumb.get_trading_fee("BTC"))

  def getBitCoinList(self, coin): #코인 리스트, 코인 정보 가져오기
    url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
    headers = {"accept": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)
    return response
  
  def getCandleStick(self, item): #차트 데이터
    dataList = []
    url = f"https://api.bithumb.com/public/candlestick/{item.id}_KRW/{item.term}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    if type(response) == dict:
      response = response['data']
      df = DataFrame(response, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
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

  def getCoinOrderBook(self, coin): #코인 거래 내역
    orderBook = self.bithumb.get_orderbook(coin)
    return orderBook

  def checkAccount(self): #보유 예수금 목록
    KRW = self.bithumb.get_balance('BTC')
    KRW = KRW[2]
    return KRW

  def setBuyCondition(self): #매수 조건
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

  def getMyCoinList(self): #현재 보유 코인 종류
    coinList = self.bithumb.get_balance('All')
    coinList = coinList['data']
    coinTotalList = dict.items(coinList)
    totalList = []
    myCoinList = []
    for item in coinTotalList:
      if( 'total_' in str(item[0])):
        totalList.append(item)
    for item in totalList:
      if( float(item[1]) >= 0.0001 ):
        if item[0] != 'total_krw': 
          if item[0] != 'total_bm':
            myCoinList.append(item)
    return myCoinList

  def getTransactionHistory(self, target): # 거래내역
    print(self.bithumb.get_transaction_history(target))

  def getOrderCompleted(self):
    print(self.bithumb.get_order_completed())

  def getBuyPrice(self, coin):
    buyPrice = self.bithumb.get_orderbook(coin)['bids'][1]['price']
    print(buyPrice)
    return buyPrice
    
  def buyQuantity (self, buyPrice ) :
    buy_quantity = self.checkAccount() *  0.9970 / buyPrice # 수수료 0.25% 계산
    buy_quantity = float ( "{:.4f}".format(buy_quantity) )  # 소수점 4자리 수 버림
    print ( self.checkAccount(), buyPrice, buy_quantity)
    return buy_quantity
  
  def bulkSale(self):
    coinList = self.getMyCoinList()
    for coin in coinList:
      coinName = (str(coin[0]).replace('total_',""))
      if(coinName != 'krw'):
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
      coinInfo = self.getBitCoinList(str(i[0]).replace('total_',""))
      coinValue = float(coinInfo['data']['closing_price']) * round(float(i[1]), 4)
      list.append(coinValue)
    for index in range(len(list)):
      money += list[index]
    account = self.checkAccount()
    money += account
    return money
  
## 거래 내역 조회 및 검색 기능
  async def getOrderList(self, page):
    count = "14"
    if(page == 1):
      prev = "0"
    else:
      prev = str((int(page) - 1) * 15)
    selectData = await self.mysql.Select(orderListSql(count, prev))
    orderList = []
    for data in selectData:
      orderDesc = (data[2], data[1], data[3], 'KRW')
      print(self.bithumb.get_order_completed(orderDesc))
      orderList.append(self.bithumb.get_order_completed(orderDesc)['data'])
    return orderList
  
  def getDateOrderList(self, date, page):
    count = "14"
    if(page == 1):
      prev = "0"
    else:
      prev = str((int(page) - 1) * 15)
    selectData = self.mysql.Select(dateOrderListSql(count, prev, date[0], date[1]))
    orderList = []
    for data in selectData:
      orderDesc = (data[2], data[1], data[3], 'KRW')
      orderList.append(self.bithumb.get_order_completed(orderDesc)['data'])
    return orderList

## Dash Page
  async def dashProperty(self, date):
    coinList = self.getMyCoinList()
    time.sleep(1)
    dt = datetime.now()
    print(dt)
    list = []
    fee = 0
    totalMoney = 0
    buyingMoney = 0
    sellingMoney = 0
    selectData = await self.mysql.Select(todayOrderListSql(date[0], date[1]))
    time.sleep(1)
    for i in coinList:
      coinInfo = self.getBitCoinList(str(i[0]).replace('total_',""))
      coinValue = float(coinInfo['data']['closing_price']) * round(float(i[1]), 4)
      list.append(coinValue)
    for index in range(len(list)):
      totalMoney += list[index]
    account = self.checkAccount()
    totalMoney += account
    if selectData != 333:
      for todayData in selectData:
        if todayData[2] == 'ask':
          sellingMoney += float(todayData[9])
        else:
          buyingMoney += float(todayData[9])
        fee += float(todayData[8])
      accountData = [totalMoney, account, buyingMoney, sellingMoney, fee]
      return accountData

  async def getDisparity(self, coin, disparity, trends):
    flag = True
    url = f"https://api.bithumb.com/public/candlestick/"+coin[0]+"_KRW/6h"
    headers = {"accept": "application/json"}
    data = json.loads(requests.get(url, headers=headers).text)['data']
    df = pd.DataFrame(data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
    AR = tuple(df['Close'].rolling(window = 5).mean().fillna('undefined'))
    AR_BASE = AR[-10: -1]
    BASE = df['Close'].values.tolist()
    for term in range(0, int(trends)):
      try:
        if term == 0:
          separation = (float(BASE[len(BASE) - (term + 1)]) / float(AR_BASE[len(AR_BASE) - (term + 1)])) * 100
          if separation < int(disparity):
            return ''
        result = float(BASE[len(BASE) - (term + 1)]) - float(AR_BASE[len(AR_BASE) - (term + 1)])
        if result < 0:
          flag = False
          return ''
        if flag == True:
          # return {"coin": {"coin":coin[0], "data":self.getBitCoinList(coin[0])["data"]}, "separation": separation}
          self.mysql.Insert(insertRecommendCoin, [coin[0], self.getBitCoinList(coin[0])["data"]["closing_price"]])
          self.recommandCoinList.append({"coin": {"coin":coin[0], "data":self.getBitCoinList(coin[0])["data"]}, "separation": separation})
          print("data ::::::",coin[0], self.getBitCoinList(coin[0])["data"]["closing_price"])
          return 'list append'
      except:
        return ''

  async def test(self, coinList, first_disparity, trends):
    for coin in coinList:
      self.getDisparity(coin, first_disparity, trends)

  async def getRecommendPrice(self):
    try:
      self.recommandCoinList = []
      await self.mysql.Delete(deleteRecommendCoin, [])
      getUseOption = await self.mysql.Select(selectUseSearchOptionSql)
      print("getUseOption :::::::", getUseOption[0][0])
      options = await self.mysql.Select(selectActiveSearchOptionSql(str(getUseOption[0][0])))
      print("options ::::::::: ", options)
      first_disparity = options[0][0] #이격도 1 < 검색 이격도
      second_disparity = options[0][1] # 이격도 2 > 검색 이격도
      trends = options[0][2] # 추세
      trends_idx = options[0][3] # 평균선 idx
      avg_volume = options[0][4] # 평균 거래량
      transaction_amount = options[0][5] # 거래 대금
      price = options[0][6] # 가격 
      print(first_disparity, second_disparity, trends, trends_idx, avg_volume, transaction_amount, price)
      coinList = await self.mysql.Select(getDBCoinList(price, transaction_amount))
      print("coinList :::::::::::", coinList)
      time.sleep(1)
      if len(coinList) == 0:
        return 201
      else:
        for coin in coinList:
          value = await self.getDisparity(coin, first_disparity, trends)
          if value != '':
            print("append List ! :::::::: ")
        return self.recommandCoinList
    except:
      return 333

  async def possessoionCoinInfo(self):
    try:
      possessionCoin = await self.mysql.Select(getMyCoinListSql)
      time.sleep(1)
      if len(possessionCoin) == 0:
        return 203
      returnList = []
      for coin in possessionCoin:
        coinInfo = self.getBitCoinList(coin[0])['data']
        coinValue = float(coinInfo['closing_price'])
        returnList.append({
          "coin" : coin[0], 
          "info" : { 
                  "unit" : coin[1],
                  "now_price" : coinValue,
                  "buy_price" : coin[2],
                  "buy_total_price" : coin[3],
                  "evaluate_price" : float(coinValue) * float(coin[1]), #평가금액
                  "profit" : float(coinValue) * float(coin[1]) - float(coin[3]),
                  "rate" : (float(coinValue) * float(coin[1]) - float(coin[3])) / float(coin[3]) 
                  }, 
        })
      return returnList
    except:
      return 333

# Setting Page 
  async def getDisparityOption(self):
    options = await self.mysql.Select(getDisparityOptionSql)
    options = { options[0][1]:{"idx":options[0][0], "name":options[0][1],"range":options[0][2], "color":options[0][3]},
                options[1][1]:{"idx":options[1][0], "name":options[1][1],"range":options[1][2], "color":options[1][3]},
                options[2][1]:{"idx":options[2][0], "name":options[2][1],"range":options[2][2], "color":options[2][3]} }
    return options
  
  async def updateDisparityOption(self, item):
    try:
      for data in item:
        await self.mysql.Update(updateDisparityOptionSql,[str(data[1]['range']), data[1]['color'], data[1]['name']])
        self.mysql.Insert(insertLog, [2, "이동평균선 조건 변경"])
      return 200
    except:
      return 303
  
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
        "trends_idx":data[5],
        "avg_volume": data[6], 
        "transaction_amount": data[7], 
        "price": data[8]})
    print(optionList)
    return optionList

  def insertSearchOption(self, item):
    self.mysql.Insert(insertSearchOptionSql,[
      item.name, 
      item.first_disparity, 
      item.second_disparity, 
      item.trends_idx, 
      item.trends, 
      item.avg_volume, 
      item.transaction_amount, 
      item.price
    ])
    self.mysql.Insert(insertLog,[1, "검색 조건 추가"])

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
    self.mysql.Insert(insertLog,[1, "검색 조건 뱐ㅕㅇ"])

  async def updateUseSearchOption(self, num):
    print("numnum :::::::::", num)
    try:
      await self.mysql.Update(updateUseSearchOption, [ num ])
      self.mysql.Insert(insertLog,[1, num + "으로 시용 검색 조건 변경"])
      return 200
    except:
      return 303

# Auto But and Selling

  async def buy(self, coin, unit): #매수
    buyLog = self.bithumb.buy_market_order(coin, unit) #params 1: 종목, 2: 갯수
    time.sleep(0.1)
    print(buyLog)
    if(type(buyLog) == tuple):
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
        print("myCoinList", myCoinList)
        if len(myCoinList) == 0:
          self.mysql.Insert(insertPossessionCoin,[
            buyLog[1]+'_KRW',
            detailLog['order_qty'],
            detailLog['contract'][0]['price'],
            detailLog['contract'][0]['total'],
            detailLog['contract'][0]['fee']
          ])
        else:
          start = 0
          goal = len(myCoinList)
          for myCoin in myCoinList:
            start = start + 1
            if myCoin[0] == buyLog[1]+'_KRW':
              print('Yes!!!')
              self.mysql.Insert(buyUpdatePossessionCoin,[
              str(float(detailLog['order_qty']) + float(myCoin[1])),
              str((float(detailLog['contract'][0]['price']) + float(myCoin[2]) ) / 2),
              str(float(detailLog['contract'][0]['total']) + float(myCoin[3])),
              str(float(detailLog['contract'][0]['fee']) + float(myCoin[4])),
              buyLog[1]+'_KRW',
            ])
              break
            elif goal == start:
              print('NO!!!')
              self.mysql.Insert(insertPossessionCoin,[
                buyLog[1]+'_KRW',
                detailLog['order_qty'],
                detailLog['contract'][0]['price'],
                detailLog['contract'][0]['total'],
                detailLog['contract'][0]['fee']
              ])
              break
      return 200
    else:
      return 404
    
  async def sell(self, coin, unit): #매도
    print(" coin, unit", coin, unit)
    sellLog = self.bithumb.sell_market_order(coin, unit) #params 1: 종목, 2: 갯수
    time.sleep(0.1)
    print(sellLog)
    if(type(sellLog) == tuple):
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
        sellCoin = await self.mysql.Select(getPossessionCoin(coin+'_KRW'))
        if (float(sellCoin[0][1]) - float(detailLog['order_qty'])) <= 0.00:
          await self.mysql.Delete( deletePossessionCoin, [sellCoin[0][0]] )
          print('Delete complate')
          return 200
        else:
          await self.mysql.Update(sellUpdatePossessionCoin,[
            float(sellCoin[0][1]) - float(detailLog['order_qty']),
            float(sellCoin[0][3]) - float(detailLog['contract'][0]['total']),
            sellLog[1],
          ])
          print('sell complate')
        return 200
      else:
        return 404

  def getTotalMoney(self):
    coinList = self.getMyCoinList()
    time.sleep(1)
    list = []
    totalMoney = 0
    for i in coinList:
      coinInfo = self.getBitCoinList(str(i[0]).replace('total_',""))
      coinValue = float(coinInfo['data']['closing_price']) * round(float(i[1]), 4)
      list.append(coinValue)
    for index in range(len(list)):
      totalMoney += list[index]
    account = self.checkAccount()
    totalMoney += account
    return totalMoney

  async def updateDeposit(self):
    while True:
      deposit = self.checkAccount()
      # total = self.getTotalMoney()
      self.myDeposit = deposit
      # self.myTotalMoney = total
      await asyncio.sleep(1)

  async def updatePossessionCoin(self):
    while True:
      DBPossession = await self.mysql.Select(getMyCoinListSql)
      coinNames = []
      for i in DBPossession:
        coinNames.append(i)
      self.possessionCoinList = coinNames
      await asyncio.sleep(1)
      
  async def autoSell(self):
    try:
      uri = "wss://pubwss.bithumb.com/pub/ws"
      asyncio.create_task(self.updateDeposit())
      asyncio.create_task(self.updatePossessionCoin())
      await asyncio.sleep(1)
      coinNames = []
      print("self.possessionCoinList", self.possessionCoinList)
      for i in self.possessionCoinList:
        coinNames.append(i[0])
      print("coinNames", coinNames)
      async with websockets.connect(uri, ping_interval=None) as websocket:
        while True:
          subscribe_fmt = {
              "type":"ticker", 
              "symbols": coinNames,
              "tickTypes": ["30M"]
          }
          subscribe_data = json.dumps(subscribe_fmt)
          await websocket.send(subscribe_data)
          data = await websocket.recv()
          data = json.loads(data)
          data = data.get('content')
          if type(data) == dict:
            for myCoin in self.possessionCoinList:
              if myCoin[0] == data['symbol']:
                if ((float(data['closePrice']) - float(myCoin[2])) / float(myCoin[2])) * 100 > 0.015:
                  await self.sell(str(myCoin[0]).replace("_KRW", ""), float(myCoin[1]))
                  print("BEST SELL ::::::: ",str(myCoin[0]).replace("_KRW", ""), str(myCoin[1]))
                elif (((float(data['closePrice']) - float(myCoin[2])) / float(myCoin[2])) * 100) - 100 < 99.9:
                  await self.sell(str(myCoin[0]).replace("_KRW", ""), float(myCoin[1]))
                  print("WEST SELL ::::::: ",str(myCoin[0]).replace("_KRW", ""), str(myCoin[1]))
                else:
                  print("BEST SELL ::::::: ",str(myCoin[0]).replace("_KRW", ""), str(myCoin[1]))
                  print("WEST SELL ::::::: ",((float(data['closePrice']) - float(myCoin[2])) / float(myCoin[2]) * 100) - 100 )
    except:
      print("303")

  async def updateRecommendCoinNames(self):
    while True:
      await self.getRecommendPrice()
      DBRecommendCoin = await self.mysql.Select(selectRecommendCoin)
      coinNames = []
      for i in DBRecommendCoin:
        print("getRecommendPrice DBRecommendCoin ::::::::::::", i)
        coinNames.append(i)
      self.coinNames = coinNames
      await asyncio.sleep(60 * 8)

  async def autoBuy(self):
    try:
      uri = "wss://pubwss.bithumb.com/pub/ws"
      # await self.getRecommendPrice()
      coinNames = []
      asyncio.create_task(self.updateDeposit())
      asyncio.create_task(self.updateRecommendCoinNames())
      await asyncio.sleep(1)
      for i in self.coinNames:
        coinNames.append(i[0])
      print("coinNames ::::::::::::: ", coinNames)
      async with websockets.connect(uri, ping_interval=None) as websocket:
        while True:
          subscribe_fmt = {
              "type":"ticker", 
              "symbols": coinNames,
              "tickTypes": ["30M"]
          }
          subscribe_data = json.dumps(subscribe_fmt)
          await websocket.send(subscribe_data)
          data = await websocket.recv()
          data = json.loads(data)
          data = data.get('content')
          if type(data) == dict:
            for candidateCoin in self.coinNames:
              if candidateCoin[0] == data['symbol']:
                if ((float(data['closePrice']) - float(candidateCoin[1])) / float(candidateCoin[1])) * 100 > 0.02:
                  if(self.myDeposit > 1000):
                    usePrice = self.myDeposit * 0.7
                    buyUnit = usePrice / float(data['closePrice'])
                    print("self.myTotalMoney", self.myTotalMoney)
                    if buyUnit * float(data['closePrice']) > 1000:
                      await self.buy(str(data['symbol']).replace("_KRW", ""), buyUnit)
                      print("BUY :::::::: ", str(data['symbol']).replace("_KRW", ""), data['closePrice'])
                    else:
                      print("최소주문 금액에 해당하지 않습니다. :::::::: ")
                  else:
                    print("예수금이 3000원 미만입니다. :::::::: ")
    except:
      print("asd")
          
  async def autoTrading(self):
    self.mysql.Insert(insertLog,[5, '자동 매매 시작'])
    await asyncio.gather(self.autoSell(), self.autoBuy())

# Coin Detail 
  async def getCoinWarning(self, coin_name):
    warning = await self.mysql.Select(selectWarningFlag(coin_name))
    warning = warning[0][0]
    print("coin_name", coin_name)
    print("warning", warning)
    return warning


  async def updateCoinWarning(self, value, coin_name):
    await self.mysql.Update(updateWarningFlag, [value, coin_name])
