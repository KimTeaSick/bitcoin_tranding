from fastapi import APIRouter
from .coinFn import CoinFn
from parameter import *

coinRouter = APIRouter(
    prefix="/coin",
    tags=['coin']
)

coin = CoinFn()

@coinRouter.get("/getBitcoinInfo")
def getBitcoinInfo():
    data = coin.bit.getBitCoinList('ALL')
    return data

@coinRouter.get("/getDetailBTCInfo/{item_id}")
def getDetailBTCInfo(item_id):
    data = coin.bit.getBitCoinList(item_id)
    return data

@coinRouter.get('/getDisparity')
async def getDisparity():
    response = await coin.getDisparityOption()
    return response

@coinRouter.post('/updateDisparity')
async def getDisparity(item: updateDisparityOptionBody):
    response = await coin.updateDisparityOption(item)
    return response

@coinRouter.post("/getAvgData")
def sendAvgData(item: getAvgDataBody):
    print("/getAvgData item :::::: ", item)
    return coin.getAvgData(item.range, item.coin, item.term)