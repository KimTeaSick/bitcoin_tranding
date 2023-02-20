from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pybithumb import Bithumb
from pandas import DataFrame
from fastapi import FastAPI
from typing import Optional
from dbConnection import *
from scheduler import *
from sql import *
import pandas as pd
import numpy as np
import schedule
import websockets
import requests
import asyncio
import time 
import json
import os 

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"]
)

load_dotenv()
secretKey = os.environ.get('SECLET_KEY')
connenctKey = os.environ.get('CONNECT_KEY')

h ="24h"
url = f"https://api.bithumb.com/public/candlestick/BTC_KRW/{h}"
headers = {"accept": "application/json"}

class BitThumbPrivate():
  def __init__(self):
    self.bithumb = Bithumb(connenctKey, secretKey)

  def callGetTradingFee(self):
    print(self.bithumb.get_trading_fee("BTC"))

  def getBitCoinList(self, coin):
    url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
    headers = {"accept": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)
    return response

  def buy(self, coin, unit):
    print(self.bithumb.buy_market_order(coin, unit)) #params 1: 종목, 2: 갯수
    print('buy')

  def sell(self, coin, unit):
    print(self.bithumb.sell_market_order(coin, unit)) #params 1: 종목, 2: 갯수
    print('sell')

  def getCandleStick(self, item):
    dataList = []
    url = f"https://api.bithumb.com/public/candlestick/{item.id}_KRW/{item.term}"
    headers = {"accept": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)['data']
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
    return _d

  def getCoinOrderBook(self, coin):
    orderBook = self.bithumb.get_orderbook(coin)
    print(orderBook)
    return orderBook

  def checkAccount(self):
    KRW = self.bithumb.get_balance('BTC')[2]
    print(KRW, '원')
    return KRW

  def setBuyCondition(self):
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

  def getMyCoinList(self):
    coinList = bit.bithumb.get_balance('All')['data']
    coinTotalList = dict.items(coinList)
    totalList = []
    myCoinList = []
    for item in coinTotalList:
      if( 'total_' in str(item[0])):
        totalList.append(item)
    for item in totalList:
      if( float(item[1]) >= 0.0001 ):
        myCoinList.append(item)
    print(myCoinList)
    return myCoinList

  def getTransactionHistory(self, target):
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

  def testInsert(self, sql, val):
    mycursor = mydb.cursor(prepared=True)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    
  def show(slef):
    print("1")
    return

  def Insert1m(self):
    schedule.every(3).seconds.do(self.show)
    time.sleep(1)
    return

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



bit = BitThumbPrivate()

bit.coinNameList()
# while True:

class Item(BaseModel):
  id:  Optional[str] = None
  term: Optional[str] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/getBitcoinInfo")
def getBitcoinInfo():
  data = bit.getBitCoinList('ALL')
  return data

@app.get("/getDetailBTCInfo/{item_id}")
def getDetailBTCInfo(item_id):
  data = bit.getBitCoinList(item_id)
  return data

@app.post("/getCandleChart")
def getCandleStick(item: Item):
  print(item)
  data = bit.getCandleStick(item)
  return data

@app.get("/checkAccount")
def checkAccount():
  balance =  bit.checkAccount()
  myCoinList = bit.getMyCoinList()
  return (balance, myCoinList)

@app.get("/ws")
async def main():
  data = await bit.bithumb_ws_client()
  data = await bit.Insert1m()
  return data