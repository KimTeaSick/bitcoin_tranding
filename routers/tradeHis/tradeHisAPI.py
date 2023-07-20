import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back")

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