from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pagiNation import PagiNation
from BitThumbPrivate import *
from mongoDB import MongoDB
from dbConnection import *
from parameter import *
from sql import *
import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bit = BitThumbPrivate()
mongo = MongoDB()
page = PagiNation()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getBitcoinInfo")
def getBitcoinInfo():
    data = bit.getBitCoinList('ALL')
    return data


@app.get("/getDetailBTCInfo/{item_id}")
def getDetailBTCInfo(item_id):
    data = bit.getBitCoinList(item_id)
    return data


@app.post("/getCandleChart")
def getCandleStick(item: GetCandleStickBody):
    print("getCandleChart item", item)
    data = bit.getCandleStick(item)
    return data


@app.get("/checkAccount")
def checkAccount():
    balance = bit.checkAccount()
    myCoinList = bit.getMyCoinList()
    return (balance, myCoinList)


@app.get("/ws")
async def main():
    data = await bit.bithumb_ws_client()
    data = await bit.Insert1m()
    return data


@app.post("/sell")
async def sell(item: BuyAndSell):
    print("item", item)
    res = await bit.sell(item.coin, float(item.unit))
    return res


@app.post("/buy")
async def buy(item: BuyAndSell):
    res = await bit.buy(item.coin, float(item.price), float(item.unit))
    return res


@app.get("/myProperty")# 예수금 / 자산현황
def myProperty():
    return bit.myProperty()


@app.post('/getOrderList')
async def getOrderList(item: getOrderListBody):
    pageCount = await page.orderListPageCount()
    data = await bit.getOrderList(item.page)
    return {"data": data, "page": pageCount}


@app.post('/getDateOrderList')
def getDateOrderList(item: getDateOrderListBody):
    # return bit.getDateOrderList(item.date, item.page)
    return {"data": bit.getDateOrderList(item.date, item.page), "page": 1}


@app.post("/getAvgData")
def sendAvgData(item: getAvgDataBody):
    return mongo.getAvgData(item.range, item.coin, item.term)


@app.post("/dash/getRecommendCoin")
async def getRecommendPrice(item: getRecommendOption):
    now1 = datetime.datetime.now()
    response = await bit.getRecommendCoin(item)
    now2 = datetime.datetime.now()
    print(now2 - now1)

    return response


@app.get("/dash/getPossessoionCoinInfo")
async def getPossessoionCoinInfo():
    response = await bit.possessoionCoinInfo()
    return response


@app.get('/dash/accountInfo/')
async def getAccountInfo(date1, date2):
    try:
        response = await bit.dashProperty([str(date1), str(date2)])
        return response
    except:
        return 404


@app.post('/autotrading')
async def autoTrading():
    await bit.autoTrading()


@app.post('/setting/updateUseSearchOption')
async def updateUseSearchOption(item: updateUseSearchOptionBody):
    return await bit.updateUseSearchOption(item.num)


@app.get('/setting/getDisparity')
async def getDisparity():
    response = await bit.getDisparityOption()
    return response


@app.post('/setting/updateDisparity')
async def getDisparity(item: updateDisparityOptionBody):
    response = await bit.updateDisparityOption(item)
    return response


@app.get('/setting/getSearchOptionList')
async def getSearchOptionList():
    response = await bit.getSearchOptionList()
    return response


@app.post('/setting/registerSearchOption')
def insertSearchOption(item: updateSearchOptionBody):
    response = bit.insertSearchOption(item)
    return response


@app.post('/setting/updateSearchOption')
async def updateSearchOption(item: updateSearchOptionBody):
    response = await bit.updateSearchOption(item)
    return response


@app.post('/option/insertOption')
async def updateSearchOption(item: insertOption):
    response = await bit.insertOption(item)
    return response


@app.get('/option/optionList')
async def getOptionList():
    response = await bit.optionList()
    return response


@app.post('/option/optionDetail')
async def selectOptionDetail(item: getOptionDetail):
    response = await bit.optionDetail(item)
    return response


@app.post('/option/updateOption')
async def UpdateOption(item: updateOption):
    response = await bit.updateOption(item)
    return response


@app.post('/option/deleteOption')
async def OptionDelete(item: deleteOption):
    response = await bit.deleteOption(item)
    return response


@app.post('/option/useOption')
async def OptionUsed(item: useOption):
    response = await bit.useOption(item)
    return response


@app.post('/trade/insertTradingOption')
async def OptionUsed(item: tradingOption):
    response = await bit.insertTradingOPtion(item)
    return response


@app.get('/trade/tradingOptionList')
async def getOptionList():
    response = await bit.tradingOptionList()
    return response


@app.post('/trade/tradingOptionDetail')
async def selectOptionDetail(item: getTradingOptionDetail):
    response = await bit.tradingOptionDetail(item)
    return response


@app.post('/trade/updateTradingOption')
async def UpdateOption(item: tradingOption):
    response = await bit.updateTradingOption(item)
    return response


@app.post('/trade/deleteTradingOption')
async def OptionDelete(item: deleteTradingOption):
    response = await bit.deleteTradingOption(item)
    return response


@app.post('/option/useTradingOption')
async def OptionUsed(item: useTradingOption):
    response = await bit.useTradingOption(item)
    return response
