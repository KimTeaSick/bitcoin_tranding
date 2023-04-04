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
async def getOrderList(item: getOrderListBody):
  pageCount = await page.orderListPageCount()
  data = await bit.getOrderList(item.page)
  return {"data": data, "page": pageCount}

@app.post('/getDateOrderList')
def getDateOrderList(item: getDateOrderListBody):
  print(item)
  # return bit.getDateOrderList(item.date, item.page)
  return {"data": bit.getDateOrderList(item.date, item.page), "page": 1}

@app.post("/getAvgData")
def sendAvgData(item: getAvgDataBody):
  return mongo.getAvgData(item.range, item.coin, item.term)

@app.get("/dash/getRecommendPrice")
async def getRecommendPrice():
  response = await bit.getRecommendPrice()
  return response

@app.get("/dash/getPossessoionCoinInfo")
async def getPossessoionCoinInfo():
  response = await bit.possessoionCoinInfo()
  return response 

@app.get('/dash/accountInfo/')
async def getAccountInfo(date1, date2):
  response = await bit.dashProperty([str(date1), str(date2)])
  return response

@app.post('/autotrading')
async def autoTrading():
  await bit.autoTrading()

@app.get('/setting/getDisparity')
async def getDisparity():
  response = await bit.getDisparityOption()
  return response

@app.post('/setting/registerSearchOption')
async def insertSearchOption(item: getSearchOptionBody):
  print("item", item)
  response = await bit.insertSearchOption(item)
  return response

@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: getSearchOptionBody):
  response = await bit.updateSearchOption(item)
  return response