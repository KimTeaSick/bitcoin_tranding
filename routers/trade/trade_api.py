from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .parameter import *
from .trade_fn import TradeFn
from utils import insertLog
from utils.errorList import error_list

router = APIRouter(
    prefix="/trade",
    tags=["trade"]
)

trade = TradeFn()

@router.post('/insertTradingOption')
async def OptionUsed(item: insetTradingOption):
    try:
        data = await trade.insertTradingOPtion(item)
        insertLog.log("매매 옵션 등록 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("매매 옵션 등록 기능 사용 실패")
        return error_list(2)

@router.get('/tradingOptionList')
async def getOptionList(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.tradingOptionList(request.state.idx)
        insertLog.log("매매 옵션 조회 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("매매 옵션 조회 기능 사용 실패")
        return error_list(2)

@router.post('/tradingOptionDetail')
async def selectOptionDetail(item: getTradingOptionDetail):
    try:
        data = await trade.tradingOptionDetail(item)
        insertLog.log("매매 옵션 상세 조회 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("매매 옵션 상세 조회 기능 사용 실패")
        return error_list(2)

@router.post('/updateTradingOption')
async def UpdateOption(item: tradingOption):
    try:
        data = await trade.updateTradingOption(item)
        insertLog.log("매매 옵션 수정 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("매매 옵션 수정 기능 사용 실패")
        return error_list(2)

@router.post('/deleteTradingOption')
async def OptionDelete(item: deleteTradingOption):
    try:
        data = await trade.deleteTradingOption(item)
        insertLog.log("매매 옵션 삭제 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("매매 옵션 삭제 기능 사용 실패")
        return error_list(2)


@router.post('/useTradingOption')
async def OptionUsed(item: useTradingOption, request:Request):
    try:
        data = await trade.useTradingOption(item, request.state.idx)
        insertLog.log("매매 옵션 사용 등록 기능 사용")
        return {"status": 200, "data":data}
    except Exception as e:
        print("useTradingOption Error ::: ::: ", e)
        insertLog.log("매매 옵션 사용 등록 기능 사용 실패")
        return error_list(2)


@router.get("/orderList")
async def getoderList(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.getATOrderList(request.state.bit, request.state.idx)
        return {"status": 200, "data":data}
    except Exception as e:
        print("trade orderList Error ::: :::", e)

@router.get('/getSearchPriceList')
async def getSearchList(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.getSearchPriceList(request.state.idx)
        insertLog.log("검색 종목 조회 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("검색 종목 조회 기능 사용 실패")
        return error_list(2)

@router.get('/getNowUsedCondition')
async def getNowUsedCondition(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.getNowUseCondition(request.state.idx, request.state.bit)
        insertLog.log("현재 사용 옵션 조회 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("현재 사용 옵션 조회 기능 사용 실패")
        return error_list(2)

@router.get('/getTradingHis')
async def getTradingHis(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.getTradingHis(request.state.bit, request.state.idx)
        insertLog.log("자동 매매 거래 내역 조회 기능 사용")
        return {"status": 200, "data":data}
    except:
        insertLog.log("자동 매매 거래 내역 조회 기능 사용 실패")
        return error_list(2)

@router.get('/autoTradingCheck')
async def autoTradingCheck(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.nowAutoStatusCheck(request.state.bit)
        return {"status": 200, "data":data}
    except:
        insertLog.log("자동 매매 플래그 기능 사용 실패")
        return error_list(2)

@router.post('/controlAutoTrading')
async def controlAutoTrading(item: controlAT,request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        if item.flag == 1:
            data = await trade.autoTradingOn(request.state.idx)
            insertLog.log("자동 매매 컨트롤 가동 기능 사용")
            return {"status": 200, "data": data}
        elif item.flag == 0:
            data = await trade.autoTradingOff(request.state.bit, request.state.idx)
            insertLog.log("자동 매매 컨트롤 정지 기능 사용")
            return {"status": 200, "data": data}
    except:
        insertLog.log("자동 매매 컨트롤 기능 사용 실패")
        return error_list(2)
    
@router.post('/sell')
async def controlAutoTrading(item: sellInfoBody,request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await trade.sellFn(request.state.bit,request.state.idx, item)
        return {"status": 200, "data": data}
    except:
        return error_list(2)