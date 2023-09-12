from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from routers.dashborad import dashApi
from routers.coinList import coinApi
from routers.tradeHis import tradeHisApi
from routers.search import searchApi
from routers.trade import tradeApi
from routers.test import testApi
from routers.user import userApi
from routers.assets import assetsApi
# from search_option import search
# from BitThumbPrivate import *
from lib.pagiNation import PagiNation
from lib.errorList import error_list
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
    path = request.url.path
    pass_path = ["/user/login", "/user/register", "/test/test", "/test/signTrade"] 
    if path in pass_path:
        response = await call_next(request)
        return response
    authorization_header = request.headers.get("Authorization")
    if authorization_header != 'Bearer null' and authorization_header != None:
        # print("in if ::: :::", authorization_header)
        bit = await token_validator(request)
        if bit != 401:
            idx = bit[1]
            bit = bit[0]
            request.state.bit = bit
            request.state.idx = idx
            request.state.valid_token = True
        else:
            request.state.valid_token = False
            # print("in if else ::: :::", authorization_header)
    else:
        request.state.valid_token = False
        # print("else ::: :::", authorization_header)

    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/getCandleChart")
def getCandleStick(item: GetCandleStickBody, request: Request):
    try:
        data = request.state.bit.getCandleStick(item)
        return {"status":200, "data": data}
    except Exception as e:
        return error_list(2)

@app.get("/checkAccount")
def checkAccount(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    balance = request.state.bit.checkAccount()
    myCoinList = request.state.bit.getMyCoinList()
    return {"status": 200, "data": (balance, myCoinList)}

@app.post("/sell")
async def sell(item: BuyAndSell, request: Request):
    print("item", item)
    data = await request.state.bit.sell(item.coin, float(item.unit))
    return data

@app.post("/buy")
async def buy(item: BuyAndSell, request: Request):
    data = await request.state.bit.buy(item.coin, float(item.price), float(item.unit))
    return data

@app.get("/myProperty")# 예수금 / 자산현황
def myProperty(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    data = request.state.bit.myProperty()
    return { "status":200, "data": data }

@app.get('/setting/getSearchOptionList')
async def getSearchOptionList(request: Request):
    data = await request.state.bit.getSearchOptionList()
    return { "status":200, "data": data }

@app.post('/setting/registerSearchOption')
def insertSearchOption(item: updateSearchOptionBody, request: Request):
    data = request.state.bit.insertSearchOption(item)
    return { "status":200, "data": data }

@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: updateSearchOptionBody, request: Request):
    data = await request.state.bit.updateSearchOption(item)
    return { "status":200, "data": data }

@app.get('/todayAccount')
async def todayAccount(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    data = await request.state.bit.todayAccount(request.state.idx)
    return { "status":200, "data": data }

@app.get("/nowRate")
async def nowRate(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    data = await request.state.bit.nowRate(request.state.idx)
    return { "status":200, "data": data }

@app.get("/coinlist.json")
async def getCoinJsonFile(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    data = await request.state.bit.getBithumbCoinList()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir_path :::: ", dir_path)
    return { "status":200, "data": data }

app.include_router(userApi.userRouter)
app.include_router(dashApi.dashRouter)
app.include_router(coinApi.coinRouter)
app.include_router(tradeHisApi.tradeRouter)
app.include_router(searchApi.searchRouter)
app.include_router(tradeApi.tradeRouter)
app.include_router(assetsApi.assetsRouter)
app.include_router(testApi.testRouter)

if __name__ == "__main__":
    config = uvicorn.Config("ncbithumb:app", port=8888, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
