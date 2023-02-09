from dotenv import load_dotenv
from pybithumb import Bithumb
import os 
import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

  def getCandleStick(self, coin):
    df = Bithumb.get_candlestick(coin, chart_intervals="1m")
    print(df.tail(5400))
    return df

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


bit = BitThumbPrivate()
bit.getCandleStick('BTC')

# while True:

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

@app.get("/getCandleChart/{item_id}")
def getCandleStick(item_id):
  data = bit.getCandleStick(item_id)
  return data

