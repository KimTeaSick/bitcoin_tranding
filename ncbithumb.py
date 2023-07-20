from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers.dashborad import dashApi
from routers.coinList import coinApi
from routers.tradeHis import tradeHisApi
from routers.search import searchApi
from routers.trade import tradeApi
from search_option import search
from lib.pagiNation import PagiNation
from BitThumbPrivate import *
from mongoDB import MongoDB
from dbConnection import *
from parameter import *
from sqld import *
import datetime
import uvicorn
import os

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bit = BitThumbPrivate()
page = PagiNation()
mongo = MongoDB()
mysql = MySql()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/getCandleChart")
def getCandleStick(item: GetCandleStickBody):
    print("getCandleChart item", item)
    data = bit.getCandleStick(item)
    return data

@app.get("/checkAccount")
def checkAccount():
    balance = bit.checkAccount()
    myCoinList = bit.getMyCoinList()
    return (balance, myCoinList)

@app.post("/sell")
async def sell(item: BuyAndSell):
    print("item", item)
    res = await bit.sell(item.coin, float(item.unit))
    return res

@app.post("/buy")
async def buy(item: BuyAndSell):
    res = await bit.buy(item.coin, float(item.price), float(item.unit))
    return res

@app.get("/myProperty")# 예수금 / 자산현황
def myProperty():
    return bit.myProperty()

@app.get('/setting/getSearchOptionList')
async def getSearchOptionList():
    response = await bit.getSearchOptionList()
    return response

@app.post('/setting/registerSearchOption')
def insertSearchOption(item: updateSearchOptionBody):
    response = bit.insertSearchOption(item)
    return response

@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: updateSearchOptionBody):
    response = await bit.updateSearchOption(item)
    return response

@app.get('/todayAccount')
async def todayAccount():
    response = await bit.todayAccount()
    return response

@app.get("/nowRate")
async def nowRate():
    response = await bit.nowRate()
    return response

@app.get("/coinlist.json")
async def getCoinJsonFile():
    response = await bit.getBithumbCoinList()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir_path :::: ", dir_path)
    return response

@app.post("/newRawSearch")
async def newSearch(item: newSearchBody):
    response = await search.raw_search(item)
    return response

@app.post("/newSearch")
async def newSearch():
    response = await search.search()
    return response

app.include_router(dashApi.dashRouter)
app.include_router(coinApi.coinRouter)
app.include_router(tradeHisApi.tradeRouter)
app.include_router(searchApi.searchRouter)
app.include_router(tradeApi.tradeRouter)

if __name__ == "__main__":
    config = uvicorn.Config("ncbithumb:app", port=8888, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
