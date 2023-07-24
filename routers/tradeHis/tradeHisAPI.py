from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from lib.pagiNation import PagiNation
from fastapi import APIRouter
from .parameter import *
from .tradeHisFn import TradeHisFn

tradeRouter = APIRouter(
    prefix='/tradeHis',
    tags=['tradeHis']
)

tradeHis = TradeHisFn()

@tradeRouter.post('/getOrderList')
async def getOrderList(item: getOrderListBody):
    pageCount = await tradeHis.orderListPageCount()
    data = await tradeHis.getOrderList(item.page)
    return {"data": data, "page": pageCount}