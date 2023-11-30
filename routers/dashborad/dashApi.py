from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .dashFn import DashBoardFn
from .parameter import *
from utils import insertLog
from utils.errorList import error_list

dash = DashBoardFn()

dashRouter = APIRouter(
    prefix="/dash",
    tags=["dash"]
)

@dashRouter.get('/getPossessoionCoinInfo')
async def getPossessoionCoinInfo(request: Request):
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
        data = await dash.rateCheck(item, request.state.bit, request.state.idx)
        return {"status":200, "data": data}
    except Exception as e:
        print("rateCheck Error ::: :::", e)
        return error_list(2)
    
@dashRouter.get('/all_user_deposit')
async def all_user_deposit_api(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.all_user_deposit_fn()
        return {"status":200, "data": data}
    except Exception as e:
        print("all_user_deposit_api Error ::: :::", e)
        return error_list(2)
    
# @dashRouter.post("/get_users_rate_info")
# async def get_users_rate_info_Api(item:onlyIdx ,request: Request):
#     if request.state.valid_token != True:
#         return error_list(0)
#     try:
#         data = await dash.getUsersRateInfoFn(item.idx, request.state.bit)
#         return { "status":200 , "data": data }
#     except Exception as e:
#         print("get_users_rate_info Error ::: :::", e)
#         return error_list(2)

@dashRouter.get("/get_users_rate_info/")
async def get_users_rate_info_Api(idx:int ,request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUsersRateInfoFn(idx, request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("get_users_rate_info Error ::: :::", e)
        return error_list(2)

@dashRouter.get("/getCurrentRate/")
async def getCurrentRate(idx, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getCurrentRateFn(idx)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@dashRouter.post("/day_week_month_data")
async def day_week_month_data_api(item:onlyIdx, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.day_week_month_data_fn(item.idx ,request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("get_users_rate_info Error ::: :::", e)
        return error_list(2)

@dashRouter.get("/totalOperateMoney")
async def getTotalOperateMoney(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getTotalOperateMoney(request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@dashRouter.get("/getChartData/")
async def getChartDataApi(idx:int, term:int, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getChartDataFn(idx, term)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@dashRouter.get("/getUserCount/")
async def getUserCountApi(request: Request, now: int):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUserCountFn(request.state.bit, now)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getUserCount Error ::: ", e)

@dashRouter.get("/getUserList/")
async def getUserListApi(request: Request, now: int):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUserListFn(request.state.bit, now)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getUserCount Error ::: ", e)