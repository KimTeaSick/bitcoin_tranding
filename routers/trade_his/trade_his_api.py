from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/4season/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .parameter import *
from .trade_his_fn import TradeHisFn
from utils.errorList import error_list

router = APIRouter(
    prefix='/tradeHis',
    tags=['tradeHis']
)

tradeHis = TradeHisFn()

@router.post('/getOrderList')
async def getOrderList(item: getOrderListBody, request: Request):
    if request.state.valid_token != True:
        return error_list(0)
    pageCount = await tradeHis.orderListPageCount(request.state.idx, request.state.bit)
    data = await tradeHis.getOrderList(request.state.idx, item.page, request.state.bit)
    return { "status": 200, "data": {"data": data, "page": pageCount} }