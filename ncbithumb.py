from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pagiNation import PagiNation
from BitThumbPrivate import *
from mongoDB import MongoDB
from dbConnection import *
from parameter import *
from sql import *
import datetime
import uvicorn
import os

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
mysql = MySql()

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
    # try:
        now1 = datetime.datetime.now()
        response = await bit.getRecommendCoin(item)
        now2 = datetime.datetime.now()
        print(now2 - now1)
        mysql.Insert(insertLog,["검색 기능 사용"])
        return response
    # except:
        # mysql.Insert(insertLog,["검색 기능 사용 실패"])
        # return 444


@app.get("/dash/getPossessoionCoinInfo")
async def getPossessoionCoinInfo():
    response = await bit.possessoionCoinInfo()
    return response


@app.get('/dash/accountInfo/')
async def getAccountInfo(date1, date2):
    try:
        response = await bit.dashProperty([str(date1), str(date2)])
        print("response :::: ",response)
        return response
    except:
        return 404

@app.post('/autotrading')
async def autoTrading():
    await bit.autoTrading()

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
    try:
        response = await bit.insertOption(item)
        mysql.Insert(insertLog, ["검색 옵션 등록 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 등록 기능 사용 실패"])



@app.get('/option/optionList')
async def getOptionList():
    try:
        response = await bit.optionList()
        mysql.Insert(insertLog, ["검색 옵션 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 조회 기능 사용 실패"])
        return 444



@app.post('/option/optionDetail')
async def selectOptionDetail(item: getOptionDetail):
    try:
        response = await bit.optionDetail(item)
        mysql.Insert(insertLog, ["검색 옵션 상세 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 상세 조회 기능 사용 실패"])
        return 444



@app.post('/option/updateOption')
async def UpdateOption(item: updateOption):
    try:
        response = await bit.updateOption(item)
        mysql.Insert(insertLog, ["검색 옵션 수정 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 수정 기능 사용 실패"])
        return 444



@app.post('/option/deleteOption')
async def OptionDelete(item: deleteOption):
    try:
        response = await bit.deleteOption(item)
        mysql.Insert(insertLog, ["검색 옵션 삭제 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 삭제 기능 사용 실패"])
        return 444



@app.post('/option/useOption')
async def OptionUsed(item: useOption):
    try:
        response = await bit.useOption(item)
        mysql.Insert(insertLog, ["검색 옵션 사용 등록 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 옵션 사용 등록 기능 사용 실패"])
        return 444



@app.post('/trade/insertTradingOption')
async def OptionUsed(item: tradingOption):
    try:
        response = await bit.insertTradingOPtion(item)
        mysql.Insert(insertLog, ["매매 옵션 등록 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 등록 기능 사용 샐피"])
        return 444



@app.get('/trade/tradingOptionList')
async def getOptionList():
    try:
        response = await bit.tradingOptionList()
        mysql.Insert(insertLog, ["매매 옵션 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 조회 기능 사용 실패"])
        return 444



@app.post('/trade/tradingOptionDetail')
async def selectOptionDetail(item: getTradingOptionDetail):
    try:
        response = await bit.tradingOptionDetail(item)
        mysql.Insert(insertLog, ["매매 옵션 상세 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 상세 조회 기능 사용 실패"])
        return 444



@app.post('/trade/updateTradingOption')
async def UpdateOption(item: tradingOption):
    try:
        response = await bit.updateTradingOption(item)
        mysql.Insert(insertLog, ["매매 옵션 수정 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 수정 기능 사용 실패"])
        return 444



@app.post('/trade/deleteTradingOption')
async def OptionDelete(item: deleteTradingOption):
    try:
        response = await bit.deleteTradingOption(item)
        mysql.Insert(insertLog, ["매매 옵션 삭제 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 삭제 기능 사용 실패"])
        return 444



@app.post('/option/useTradingOption')
async def OptionUsed(item: useTradingOption):
    try:
        response = await bit.useTradingOption(item)
        mysql.Insert(insertLog, ["매매 옵션 사용 등록 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["매매 옵션 사용 등록 기능 사용 실패"])
        return 444


@app.get('/trade/getSearchPriceList')
async def getSearchList():
    try:
        response = await bit.getSearchPriceList()
        mysql.Insert(insertLog, ["검색 종목 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["검색 종목 조회 기능 사용 실패"])
        return 444


@app.get('/trade/getNowUsedCondition')
async def getNowUsedCondition():
    try:
        response = await bit.getNowUseCondition()
        mysql.Insert(insertLog, ["현재 사용 옵션 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["현재 사용 옵션 조회 기능 사용 실패"])
        return 444


@app.get('/trade/getTradingHis')
async def getTradingHis():
    try:
        response = await bit.getTradingHis()
        mysql.Insert(insertLog, ["자동 매매 거래 내역 조회 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["자동 매매 거래 내역 조회 기능 사용 실패"])
        return 444


@app.get('/trade/autoTradingCheck')
async def autoTradingCheck():
    try:
        response = await bit.nowAutoStatusCheck()
        mysql.Insert(insertLog, ["자동 매매 플래그 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["자동 매매 플래그 기능 사용 실패"])
        return 444


@app.post('/trade/controlAutoTrading')
async def controlAutoTrading(item: controlAT):
    try:
        response = await bit.controlAutoTrading(item.flag)
        mysql.Insert(insertLog, ["자동 매매 컨트롤 기능 사용"])
        return response
    except:
        mysql.Insert(insertLog, ["자동 매매 컨트롤 기능 사용 실패"])
        return 444

@app.get('/todayAccount')
async def todayAccount():
    response = await bit.todayAccount()
    return response

@app.get("/nowRate")
async def nowRate():
    response = await bit.nowRate()
    return response

@app.get("/coinlist.json")
async def getCoinJsonFile():
    response = await bit.getBithumbCoinList()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("dir_path :::: ", dir_path)
    # return FileResponse(dir_path + "/coin_list.json")
    return response

if __name__ == "__main__":
    config = uvicorn.Config("ncbithumb:app", port=8888, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
