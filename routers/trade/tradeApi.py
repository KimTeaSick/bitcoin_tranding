from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .parameter import *
from .tradeFn import TradeFn
from lib import insertLog

tradeRouter = APIRouter(
    prefix="/trade",
    tags=["trade"]
)

trade = TradeFn()

@tradeRouter.post('/insertTradingOption')
async def OptionUsed(item: tradingOption):
    try:
        response = await trade.insertTradingOPtion(item)
        insertLog.log("매매 옵션 등록 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 등록 기능 사용 실패")
        return 444

@tradeRouter.get('/tradingOptionList')
async def getOptionList(request:Request):
    try:
        response = await trade.tradingOptionList(request.state.idx)
        insertLog.log("매매 옵션 조회 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 조회 기능 사용 실패")
        return 444

@tradeRouter.post('/tradingOptionDetail')
async def selectOptionDetail(item: getTradingOptionDetail):
    try:
        response = await trade.tradingOptionDetail(item)
        insertLog.log("매매 옵션 상세 조회 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 상세 조회 기능 사용 실패")
        return 444

@tradeRouter.post('/updateTradingOption')
async def UpdateOption(item: tradingOption):
    try:
        response = await trade.updateTradingOption(item)
        insertLog.log("매매 옵션 수정 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 수정 기능 사용 실패")
        return 444

@tradeRouter.post('/deleteTradingOption')
async def OptionDelete(item: deleteTradingOption):
    try:
        response = await trade.deleteTradingOption(item)
        insertLog.log("매매 옵션 삭제 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 삭제 기능 사용 실패")
        return 444


@tradeRouter.post('/useTradingOption')
async def OptionUsed(item: useTradingOption):
    try:
        response = await trade.useTradingOption(item)
        insertLog.log("매매 옵션 사용 등록 기능 사용")
        return response
    except:
        insertLog.log("매매 옵션 사용 등록 기능 사용 실패")
        return 444


@tradeRouter.get("/orderList")
async def getoderList(request:Request):
    response = await trade.getATOrderList(request.state.bit, request.state.idx)
    return response

@tradeRouter.get('/getSearchPriceList')
async def getSearchList(request:Request):
    try:
        response = await trade.getSearchPriceList(request.state.bit)
        insertLog.log("검색 종목 조회 기능 사용")
        return response
    except:
        insertLog.log("검색 종목 조회 기능 사용 실패")
        return 444

@tradeRouter.get('/getNowUsedCondition/')
async def getNowUsedCondition(idx,request:Request):
    try:
        response = await trade.getNowUseCondition(idx,request.state.bit)
        insertLog.log("현재 사용 옵션 조회 기능 사용")
        return response
    except:
        insertLog.log("현재 사용 옵션 조회 기능 사용 실패")
        return 444

@tradeRouter.get('/getTradingHis')
async def getTradingHis(request:Request):
    try:
        response = await trade.getTradingHis(request.state.bit, request.state.idx)
        insertLog.log("자동 매매 거래 내역 조회 기능 사용")
        return response
    except:
        insertLog.log("자동 매매 거래 내역 조회 기능 사용 실패")
        return 444

@tradeRouter.get('/autoTradingCheck')
async def autoTradingCheck(request:Request):
    try:
        response = await trade.nowAutoStatusCheck(request.state.bit)
        return response
    except:
        insertLog.log("자동 매매 플래그 기능 사용 실패")
        return 444

@tradeRouter.post('/controlAutoTrading')
async def controlAutoTrading(item: controlAT,request:Request):
    try:
        response = await trade.controlAutoTrading(item.flag, request.state.bit, request.state.idx)
        insertLog.log("자동 매매 컨트롤 기능 사용")
        return response
    except:
        insertLog.log("자동 매매 컨트롤 기능 사용 실패")
        return 444