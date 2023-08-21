from fastapi import APIRouter, Request
from .coinFn import CoinFn
from .parameter import *

coinRouter = APIRouter(
    prefix="/coin",
    tags=['coin']
)

coin = CoinFn()

@coinRouter.get("/getBitcoinInfo")
def getBitcoinInfo(request:Request):
    data = request.state.bit.getBitCoinList('ALL')
    return data

@coinRouter.get("/getDetailBTCInfo/{item_id}")
def getDetailBTCInfo(item_id, request:Request):
    data = request.state.bit.getBitCoinList(item_id)
    return data

@coinRouter.get('/getDisparity')
async def getDisparity(request:Request):
    response = await coin.getDisparityOption(request.state.bit)
    return response

@coinRouter.post('/updateDisparity')
async def getDisparity(item: updateDisparityOptionBody, request:Request):
    response = await coin.updateDisparityOption(item, request.state.bit)
    return response

@coinRouter.post("/getAvgData")
def sendAvgData(item: getAvgDataBody, request:Request):
    print("/getAvgData item :::::: ", item)
    return coin.getAvgData(item.range, item.coin, item.term, request.state.bit)