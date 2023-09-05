import datetime
from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter,Request
from .dashFn import DashBoardFn
from .parameter import *
from lib import insertLog
from lib.errorList import error_list

dash = DashBoardFn()

dashRouter = APIRouter(
    prefix="/dash",
    tags=["dash"]
)

@dashRouter.get('/getPossessoionCoinInfo/')
async def getPossessoionCoinInfo(request: Request):
    print("request.state.valid_token", request.state.valid_token)
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.possessoionCoinInfo(request.state.idx, request.state.bit)
        return {"status":200, "data":data }
    except Exception as e:
        print("getPossessoionCoinInfo Error ::: :::", e)
        return error_list(2)

@dashRouter.post("/getRecommendCoin")
async def getRecommendPrice(item: getRecommendOption, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await request.state.bit.getRecommendCoin(item)
        insertLog.log("검색 기능 사용")
        return {"status":200, "data":data }
    except Exception as e:
        print("getRecommendCoin Error ::: ::: ", e)
        return error_list(2)

@dashRouter.get('/accountInfo/')
async def getAccountInfo(date1, date2, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.dashProperty([str(date1), str(date2)], request.state.bit)
        return {"status":200, "data":data }
    except Exception as e:
        print("getAccountInfo Error ::: :::", e)
        return error_list(2)
    
@dashRouter.post('/rateCheck')
async def test(item: rateCheckBody, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.rate_check(item, request.state.bit, request.state.idx)
        return {"status":200, "data": data}
    except Exception as e:
        print("rateCheck Error ::: :::", e)
        return error_list(2)
    
@dashRouter.get("/get_users_rate_info")
async def get_users_rate_info_Api(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.get_users_rate_info_Fn(request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("get_users_rate_info Error ::: :::", e)
        return error_list(2)
