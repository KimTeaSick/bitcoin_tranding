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
async def getDetailBTCInfo(item_id):
  data = bit.getBitCoinList(item_id)
  data["data"]["warning"] =  await bit.getCoinWarning(item_id+"_KRW")
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
async def sell(item:BuyAndSell):
  print("item",item)
  res = await bit.sell(item.coin, float(item.unit))
  return res

@app.post("/buy")
async def buy(item:BuyAndSell):
  res = await bit.buy(item.coin, float(item.unit))
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
  # return bit.getDateOrderList(item.date, item.page)
  return {"data": bit.getDateOrderList(item.date, item.page), "page": 1}

@app.post("/getAvgData")
def sendAvgData(item: getAvgDataBody):
  print("item: getAvgDataBody", item)
  return mongo.getAvgData(item.range, item.coin, item.term)

@app.get("/dash/recommendCoin")
async def getRecommendCoin():
  response = await bit.getRecommendCoin()
  return response

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

@app.post('/setting/updateUseSearchOption')
async def updateUseSearchOption(item:updateUseSearchOptionBody):
  return await bit.updateUseSearchOption(item.num)

@app.get('/setting/getDisparity')
async def getDisparity():
  response = await bit.getDisparityOption()
  return response

@app.post('/setting/updateDisparity')
async def getDisparity(item: updateDisparityOptionBody):
  response = await bit.updateDisparityOption(item)
  return response

@app.get('/setting/getSearchOptionList')
async def getSearchOptionList():
  response = await bit.getSearchOptionList()
  return response

@app.post('/setting/registerSearchOption')
def insertSearchOption(item: updateSearchOptionBody):
  print(item)
  response = bit.insertSearchOption(item)
  return response

@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: updateSearchOptionBody):
  response = await bit.updateSearchOption(item)
  return response

@app.post("/coinDetail/updateWarning")
async def updateWarning(item: updateCoinWarning):
  try:
    await bit.updateCoinWarning(item.value, item.coin_name)
    return 200
  except:
    return 303