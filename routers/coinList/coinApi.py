from fastapi import APIRouter, Request
from .coinFn import CoinFn
from .parameter import *
from lib.errorList import error_list

coinRouter = APIRouter(
    prefix="/coin",
    tags=['coin']
)

coin = CoinFn()

@coinRouter.get("/getBitcoinInfo")
def getBitcoinInfo(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = request.state.bit.getBitCoinList('ALL')
        return {"status":200, "data":data}
    except Exception as e:
        print("getBitcoinInfo Error ::: ::: ", e)
        return error_list(2)

@coinRouter.get("/getDetailBTCInfo/{item_id}")
def getDetailBTCInfo(item_id, request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = request.state.bit.getBitCoinList(item_id)
        warning = coin.get_warning_fn(item_id)
        data = data["data"]
        data['warning'] = warning
        return {"status":200, "data":data}
    except Exception as e:
        print("getDetailBTCInfo", e)
        return error_list(2)

@coinRouter.get('/getDisparity')
async def getDisparity(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await coin.getDisparityOption(request.state.bit)
        return {"status":200, "data":data}
    except Exception as e:
        print("getDisparity Error ::: :::", e)
        return error_list(2)

@coinRouter.post('/updateDisparity')
async def getDisparity(item: updateDisparityOptionBody, request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await coin.updateDisparityOption(item, request.state.bit)
        return {"status":200, "data":data}
    except Exception as e:
        print("updateDisparity Error ::: :::", e)
        return error_list(2)

@coinRouter.post("/getAvgData")
def sendAvgData(item: getAvgDataBody, request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = coin.getAvgData(item.range, item.coin, item.term, request.state.bit)
        return {"status":200, "data": data}
    except Exception as e:
        print("getAvgData Error ::: :::", e)
        return error_list(2)

@coinRouter.post("/updateWarning")
def update_warning_api(item: update_coin_warning_body, request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = coin.update_warning_fn(item)
        return {"status":200, "data": data}
    except Exception as e:
        print("getAvgData Error ::: :::", e)
        return error_list(2)
