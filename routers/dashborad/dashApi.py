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

dash = DashBoardFn()

dashRouter = APIRouter(
    prefix="/dash",
    tags=["dash"]
)

@dashRouter.get('/getPossessoionCoinInfo/')
async def getPossessoionCoinInfo(request: Request):
    response = await dash.possessoionCoinInfo(request.state.idx, request.state.bit)
    return response

@dashRouter.post("/getRecommendCoin")
async def getRecommendPrice(item: getRecommendOption, request: Request):
    now1 = datetime.datetime.now()
    response = await request.state.bit.getRecommendCoin(item)
    now2 = datetime.datetime.now()
    print(now2 - now1)
    insertLog.log("검색 기능 사용")
    return response

@dashRouter.get('/accountInfo/')
async def getAccountInfo(date1, date2, request: Request):
    try:
        response = await dash.dashProperty([str(date1), str(date2)], request.state.bit)
        return response
    except:
        return 404
    
@dashRouter.post('/rateCheck')
async def test(item: rateCheckBody, request: Request):
    res = await dash.rate_check(item, request.state.bit, request.state.idx)
    print("res", res)
    return {'rate': res[0], 'account_balance': res[1]}