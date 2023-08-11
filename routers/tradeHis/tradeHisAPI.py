from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from lib.pagiNation import PagiNation
from fastapi import APIRouter, Request
from .parameter import *
from .tradeHisFn import TradeHisFn

tradeRouter = APIRouter(
    prefix='/tradeHis',
    tags=['tradeHis']
)

tradeHis = TradeHisFn()

@tradeRouter.post('/getOrderList')
async def getOrderList(item: getOrderListBody, req: Request):
    pageCount = await tradeHis.orderListPageCount(req.state.idx, req.state.bit)
    data = await tradeHis.getOrderList(req.state.idx, item.page, req.state.bit)
    return {"data": data, "page": pageCount}