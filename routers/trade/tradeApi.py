import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back")

from fastapi import APIRouter
from parameter import *
from .tradeFn import TradeFn
from sql import *

tradeRouter = APIRouter(
    prefix="/trade",
    tags=["trade"]
)

trade = TradeFn()

@tradeRouter.post('/insertTradingOption')
async def OptionUsed(item: tradingOption):
    try:
        response = await trade.insertTradingOPtion(item)
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 등록 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 등록 기능 사용 샐피"])
        return 444

@tradeRouter.get('/tradingOptionList')
async def getOptionList():
    try:
        response = await trade.bit.tradingOptionList()
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 조회 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 조회 기능 사용 실패"])
        return 444

@tradeRouter.post('/tradingOptionDetail')
async def selectOptionDetail(item: getTradingOptionDetail):
    try:
        response = await trade.tradingOptionDetail(item)
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 상세 조회 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 상세 조회 기능 사용 실패"])
        return 444

@tradeRouter.post('/updateTradingOption')
async def UpdateOption(item: tradingOption):
    try:
        response = await trade.updateTradingOption(item)
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 수정 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 수정 기능 사용 실패"])
        return 444

@tradeRouter.post('/deleteTradingOption')
async def OptionDelete(item: deleteTradingOption):
    try:
        response = await trade.deleteTradingOption(item)
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 삭제 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 삭제 기능 사용 실패"])
        return 444


@tradeRouter.post('/useTradingOption')
async def OptionUsed(item: useTradingOption):
    try:
        response = await trade.useTradingOption(item)
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 사용 등록 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["매매 옵션 사용 등록 기능 사용 실패"])
        return 444


@tradeRouter.get("/orderList")
async def getoderList():
    response = await trade.getATOrderList()
    return response

@tradeRouter.get('/getSearchPriceList')
async def getSearchList():
    try:
        response = await trade.getSearchPriceList()
        trade.bit.mysql.Insert(insertLog, ["검색 종목 조회 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["검색 종목 조회 기능 사용 실패"])
        return 444

@tradeRouter.get('/getNowUsedCondition')
async def getNowUsedCondition():
    try:
        response = await trade.getNowUseCondition()
        trade.bit.mysql.Insert(insertLog, ["현재 사용 옵션 조회 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["현재 사용 옵션 조회 기능 사용 실패"])
        return 444

@tradeRouter.get('/getTradingHis')
async def getTradingHis():
    try:
        response = await trade.getTradingHis()
        trade.bit.mysql.Insert(insertLog, ["자동 매매 거래 내역 조회 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["자동 매매 거래 내역 조회 기능 사용 실패"])
        return 444

@tradeRouter.get('/autoTradingCheck')
async def autoTradingCheck():
    try:
        response = await trade.nowAutoStatusCheck()
        trade.bit.mysql.Insert(insertLog, ["자동 매매 플래그 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["자동 매매 플래그 기능 사용 실패"])
        return 444

@tradeRouter.post('/controlAutoTrading')
async def controlAutoTrading(item: controlAT):
    try:
        response = await trade.controlAutoTrading(item.flag)
        trade.bit.mysql.Insert(insertLog, ["자동 매매 컨트롤 기능 사용"])
        return response
    except:
        trade.bit.mysql.Insert(insertLog, ["자동 매매 컨트롤 기능 사용 실패"])
        return 444