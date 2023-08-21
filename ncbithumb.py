from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Depends, Request
from starlette.requests import Request
from routers.dashborad import dashApi
from routers.coinList import coinApi
from routers.tradeHis import tradeHisApi
from routers.search import searchApi
from routers.trade import tradeApi
from routers.test import testApi
from routers.user import userApi
# from search_option import search
# from BitThumbPrivate import *
from lib.pagiNation import PagiNation
from middleware.token_validator import token_validator
from routers.user.userApi import user
from mongoDB import MongoDB
from dbConnection import *
from parameter import *
from sqld import *
import datetime
import uvicorn
import os

app = FastAPI()

origins = ["http://121.165.242.171:48604", "http://192.168.10.119", "http://52.78.246.119"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# bit = user
page = PagiNation()
mongo = MongoDB()
mysql = MySql()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.middleware("http")
async def middleware(request: Request, call_next):
    global bit
    bit = await token_validator(request)
    if bit != 1:
        idx = bit[1]
        bit = bit[0]
        print("middleware idx", idx)
        print("middleware bit", bit)
        request.state.bit = bit
        request.state.idx = idx
        response = await call_next(request)
        return response
    else:
        response = await call_next(request)
        return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/getCandleChart")
def getCandleStick(item: GetCandleStickBody, request: Request):
    print("getCandleChart item", item)
    data = request.state.bit.getCandleStick(item)
    return data

@app.get("/checkAccount")
def checkAccount(request: Request):
    balance = request.state.bit.checkAccount()
    myCoinList = request.state.bit.getMyCoinList()
    return (balance, myCoinList)

@app.post("/sell")
async def sell(item: BuyAndSell, request: Request):
    print("item", item)
    res = await request.state.bit.sell(item.coin, float(item.unit))
    return res

@app.post("/buy")
async def buy(item: BuyAndSell, request: Request):
    res = await request.state.bit.buy(item.coin, float(item.price), float(item.unit))
    return res

@app.get("/myProperty")# 예수금 / 자산현황
def myProperty(request: Request):
    return request.state.bit.myProperty()

@app.get('/setting/getSearchOptionList')
async def getSearchOptionList(request: Request):
    response = await request.state.bit.getSearchOptionList()
    return response

@app.post('/setting/registerSearchOption')
def insertSearchOption(item: updateSearchOptionBody, request: Request):
    response = request.state.bit.insertSearchOption(item)
    return response

@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: updateSearchOptionBody, request: Request):
    response = await request.state.bit.updateSearchOption(item)
    return response

@app.get('/todayAccount')
async def todayAccount(request: Request):
    response = await request.state.bit.todayAccount(request.state.idx)
    print("todayAccount ::: ::: ", response)
    return response

@app.get("/nowRate")
async def nowRate(request: Request):
    response = await request.state.bit.nowRate()
    return response

@app.get("/coinlist.json")
async def getCoinJsonFile(request: Request):
    response = await request.state.bit.getBithumbCoinList()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir_path :::: ", dir_path)
    return response

# @app.post("/newRawSearch")
# async def newSearch(item: newSearchBody):
#     response = await search.raw_search(item)
#     return response

# @app.post("/newSearch")
# async def newSearch():
#     response = await search.search()
#     return response

app.include_router(userApi.userRouter)
app.include_router(dashApi.dashRouter)
app.include_router(coinApi.coinRouter)
app.include_router(tradeHisApi.tradeRouter)
app.include_router(searchApi.searchRouter)
app.include_router(tradeApi.tradeRouter)
app.include_router(testApi.testRouter)

if __name__ == "__main__":
    config = uvicorn.Config("ncbithumb:app", port=8888, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
