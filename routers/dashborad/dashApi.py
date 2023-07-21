import datetime
import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back") 

from fastapi import APIRouter
from .dashFn import DashBoardFn
from .parameter import *
from lib import insertLog

dash = DashBoardFn()
dashRouter = APIRouter(
    prefix="/dash",
    tags=["dash"]
)

@dashRouter.get("/getPossessoionCoinInfo")
async def getPossessoionCoinInfo():
    response = await dash.possessoionCoinInfo()
    return response

@dashRouter.post("/getRecommendCoin")
async def getRecommendPrice(item: getRecommendOption):
    now1 = datetime.datetime.now()
    response = await dash.bit.getRecommendCoin(item)
    now2 = datetime.datetime.now()
    print(now2 - now1)
    insertLog.log("검색 기능 사용")
    return response

@dashRouter.get('/dash/accountInfo/')
async def getAccountInfo(date1, date2):
    try:
        response = await dash.dashProperty([str(date1), str(date2)])
        return response
    except:
        return 404