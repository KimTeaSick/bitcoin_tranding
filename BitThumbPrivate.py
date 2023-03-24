from dotenv import load_dotenv
from pybithumb import Bithumb
from pandas import DataFrame
from dbConnection import *
from parameter import *
from sql import *
import pandas as pd
import numpy as np
import websockets
import schedule
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

  def getMyPossessionCoinList(self):
    myCoinList = Select(getMyCoinListSql)
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

  async def bithumb_ws_client(self):
    uri = "wss://pubwss.bithumb.com/pub/ws"
    coinNames = self.coinNameList()
    async with websockets.connect(uri, ping_interval=None) as websocket:
      subscribe_fmt = {
          "type":"ticker", 
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
          print(2)

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
  
  def getOrderList(self, page):
    if(page == 1):
      count = str(int(page) * 12)
      prev = "0"
    else:
      count = str(int(page) * 12)
      prev = str((int(page) - 1) * 12)

    selectData = Select(orderListSql(count, prev))
    print("selectData",selectData)
    orderList = []
    for data in selectData:
      orderDesc = (data[2], data[1], data[3], 'KRW')
      orderList.append(self.bithumb.get_order_completed(orderDesc)['data'])
    return orderList
  
  def getRecommendPrice(self):
    priceList = []
    for coin in self.coinList:
      flag = True
      url = f"https://api.bithumb.com/public/candlestick/"+coin+"_KRW/5M"
      headers = {"accept": "application/json"}
      data = json.loads(requests.get(url, headers=headers).text)['data']
      df = pd.DataFrame(data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
      AR = tuple(df['Close'].rolling(window = 5).mean().fillna('undefined'))
      AR_BASE = AR[-10: -1]
      BASE = df['Close'].values.tolist()
      for term in range(0, 5):
        if term == 0:
          separation = (float(BASE[len(BASE) - (term + 1)]) / float(AR_BASE[len(AR_BASE) - (term + 1)])) * 100
        result = float(BASE[len(BASE) - (term + 1)]) - float(AR_BASE[len(AR_BASE) - (term + 1)])
        if result < 0:
          flag = False
          break
      if flag == True:
        priceList.append({"coin": {"coin":coin, "data":self.getBitCoinList(coin)["data"]}, "separation": separation})
    return priceList






  def possessoionCoinInfo(self):
    possessionCoin = Select(getMyCoinListSql)
    print(possessionCoin)
    if len(possessionCoin) == 0:
      return 203
    returnList = []
    for coin in possessionCoin:
      coinInfo = self.getBitCoinList(coin[0])['data']
      coinValue = float(coinInfo['closing_price'])
      print(coinValue)
      returnList.append({
        "coin" : coin[0], 
        "info" : { 
                "unit" : coin[1],
                "now_price" : coinValue,
                "buy_price" : coin[2],
                "buy_total_price" : coin[3],
                "evaluate_price" : float(coinValue) * float(coin[1]), #평가금액
                "profit" : float(coinValue) * float(coin[1]) - float(coin[3]),
                "rate" : float(coinValue) * float(coin[1]) - float(coin[3]) / float(coin[3]) 
                }, 
      })
    return returnList





  def buy(self, coin, unit): #매수
    buyLog = self.bithumb.buy_market_order(coin, unit) #params 1: 종목, 2: 갯수
    time.sleep(0.1)
    if(type(buyLog) == tuple):
      detailLog = self.bithumb.get_order_completed(buyLog)['data']
      if len(detailLog['contract']) > 0:
        Insert(insertTradingLog, [
          buyLog[0],
          buyLog[1],
          buyLog[2],
          buyLog[3],
          detailLog['order_qty'],
          detailLog['contract'][0]['price'],
          detailLog['contract'][0]['fee'],
          detailLog['contract'][0]['total'],
        ])
        myCoinList = self.getMyPossessionCoinList()
        print(myCoinList)
        if len(myCoinList) == 0:
          Insert(insertPossessionCoin,[
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
            Insert(buyUpdatePossessionCoin,[
            float(detailLog['order_qty']) + float(coin[1]),
            (float(detailLog['contract'][0]['price']) + float(coin[2]) ) / 2,
            float(detailLog['contract'][0]['total']) + float(coin[3]),
            float(detailLog['contract'][0]['fee']) + float(coin[4]),
            buyLog[1],
          ])
            break
          else:
            print('NO!!!')
            Insert(insertPossessionCoin,[
              buyLog[1],
              detailLog['order_qty'],
              detailLog['contract'][0]['price'],
              detailLog['contract'][0]['total'],
              detailLog['contract'][0]['fee']
            ])
            break
      return 200
    else:
      return 404


  def sell(self, coin, unit): #매도
    sellLog = self.bithumb.sell_market_order(coin, unit) #params 1: 종목, 2: 갯수
    time.sleep(0.1)
    print(sellLog)
    if(type(sellLog) == tuple):
      detailLog = self.bithumb.get_order_completed(sellLog)['data']
      if len(detailLog['contract']) > 0:
        Insert(insertTradingLog, [
          sellLog[0],
          sellLog[1],
          sellLog[2],
          sellLog[3],
          detailLog['order_qty'],
          detailLog['contract'][0]['price'],
          detailLog['contract'][0]['fee'],
          detailLog['contract'][0]['total'],
        ])
        myCoinList = self.getMyPossessionCoinList()
        print('Start !!!')
        for coin in myCoinList:
          print("123123", float(coin[1]) - float(detailLog['order_qty']))
          print("123123", float(coin[1]) - float(detailLog['order_qty']) < 0.00)
          if (float(coin[1]) - float(detailLog['order_qty'])) == 0.0:
            print('Yes!!!')
            Delete( deletePossessionCoin, [coin[0]] )
            break
          else:
            print('NO!!!')
            Update(sellUpdatePossessionCoin,[
              float(coin[1]) - float(detailLog['order_qty']),
              float(coin[3]) - float(detailLog['contract'][0]['total']),
              sellLog[1],
            ])
            break
        return 200
      else:
        return 404