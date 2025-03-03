from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .dash_fn import DashBoardFn
from .parameter import *
from utils import insertLog
from utils.error_list import error_list

dash = DashBoardFn()

router = APIRouter(
    prefix="/dash",
    tags=["dash"]
)

<<<<<<< HEAD:routers/dashborad/dashApi.py
# @dashRouter.get('/getPossessoionCoinInfo')
=======
# @router.get('/getPossessoionCoinInfo')
>>>>>>> bd85bc4b6ee51082127d8c6ceea798faa4ed4c0a:routers/dashborad/dash_api.py
# async def getPossessoionCoinInfo(request: Request):
#     if request.state.valid_token != True:
#         return error_list(0)
#     try:
#         data = await dash.possessoionCoinInfo(request.state.idx, request.state.bit)
#         return {"status":200, "data":data }
#     except Exception as e:
#         print("getPossessoionCoinInfo Error ::: :::", e)
#         return error_list(2)

<<<<<<< HEAD:routers/dashborad/dashApi.py
# @dashRouter.post("/getRecommendCoin")
=======
# @router.post("/getRecommendCoin")
>>>>>>> bd85bc4b6ee51082127d8c6ceea798faa4ed4c0a:routers/dashborad/dash_api.py
# async def getRecommendPrice(item: getRecommendOption, request: Request):
#     if request.state.valid_token != True:
#         return error_list(0)
#     try:
#         data = await request.state.bit.getRecommendCoin(item)
#         insertLog.log("검색 기능 사용")
#         return {"status":200, "data":data }
#     except Exception as e:
#         print("getRecommendCoin Error ::: ::: ", e)
#         return error_list(2)

@router.get('/accountInfo/')
async def getAccountInfo(date1, date2, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.dashProperty([str(date1), str(date2)], request.state.bit)
        return {"status":200, "data":data }
    except Exception as e:
        print("getAccountInfo Error ::: :::", e)
        return error_list(2)
    
@router.post('/rateCheck')
async def test(item: rateCheckBody, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.rateCheck(item, request.state.bit, request.state.idx)
        return {"status":200, "data": data}
    except Exception as e:
        print("rateCheck Error ::: :::", e)
        return error_list(2)
    
@router.get('/all_user_deposit')
async def all_user_deposit_api(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.all_user_deposit_fn()
        return {"status":200, "data": data}
    except Exception as e:
        print("all_user_deposit_api Error ::: :::", e)
        return error_list(2)
    
# @router.post("/get_users_rate_info")
# async def get_users_rate_info_Api(item:onlyIdx ,request: Request):
#     if request.state.valid_token != True:
#         return error_list(0)
#     try:
#         data = await dash.getUsersRateInfoFn(item.idx, request.state.bit)
#         return { "status":200 , "data": data }
#     except Exception as e:
#         print("get_users_rate_info Error ::: :::", e)
#         return error_list(2)

@router.get("/get_users_rate_info/")
async def get_users_rate_info_Api(idx:int ,request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUsersRateInfoFn(idx, request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("get_users_rate_info Error ::: :::", e)
        return error_list(2)

@router.get("/getCurrentRate/")
async def getCurrentRate(idx, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getCurrentRateFn(idx)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@router.post("/day_week_month_data")
async def day_week_month_data_api(item:onlyIdx, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.day_week_month_data_fn(item.idx ,request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("get_users_rate_info Error ::: :::", e)
        return error_list(2)

@router.get("/totalOperateMoney")
async def getTotalOperateMoney(request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getTotalOperateMoney(request.state.bit)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@router.get("/getChartData/")
async def getChartDataApi(idx:int, term:int, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getChartDataFn(idx, term)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getCurrentRate Error ::: ", e)

@router.get("/getUserCount/")
async def getUserCountApi(request: Request, now: int):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUserCountFn(request.state.bit, now)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getUserCount Error ::: ", e)

@router.get("/getUserList/")
async def getUserListApi(request: Request, now: int):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await dash.getUserListFn(request.state.bit, now)
        return { "status":200 , "data": data }
    except Exception as e:
        print("getUserCount Error ::: ", e)