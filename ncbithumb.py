from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pagiNation import PagiNation
from BitThumbPrivate import *
from mongoDB import MongoDB
from dbConnection import *
from parameter import *
from sql import *

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"]
)

bit = BitThumbPrivate()
mongo = MongoDB()
page = PagiNation()

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
def getCandleStick(item: GetCandleStickBody):
  print("getCandleChart item",item)
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

@app.post("/sell")
def sell(item:BuyAndSell):
  res = bit.sell(item.coin, float(item.unit))
  return res

@app.post("/buy")
def buy(item:BuyAndSell):
  res = bit.buy(item.coin, float(item.unit))
  return res

@app.get("/myProperty")
def myProperty():
  return bit.myProperty()
  
@app.post('/getOrderList')
def getOrderList(item: getOrderListBody):
  pageCount = page.orderListPageCount()
  return {"data": bit.getOrderList(item.page), "page": pageCount}

@app.post("/getAvgData")
def sendAvgData(item: getAvgData):
  return mongo.getAvgData(item.range, item.coin, item.term)