from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Request
from .parameter import *
from .search_fn import SearchFn
from utils import insertLog
from utils.errorList import error_list

router = APIRouter(
    prefix="/option",
    tags=["option"]
)

search = SearchFn()

@router.post('/insertOption')
async def updateSearchOption(item: insertOption):
    try:
        data = await search.insertOption(item)
        insertLog.log("검색 옵션 등록 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 등록 기능 사용 실패")
        return error_list(2)

@router.get('/optionList')
async def getOptionList(request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await search.optionList(request.state.idx)
        insertLog.log("검색 옵션 조회 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 조회 기능 사용 실패")
        return error_list(2)

@router.post('/optionDetail')
async def selectOptionDetail(item: getOptionDetail):
    try:
        print("item",item)
        data = await search.optionDetail(item)
        insertLog.log("검색 옵션 상세 조회 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 상세 조회 기능 사용 실패")
        return error_list(2)

@router.post('/updateOption')
async def UpdateOption(item: updateOption):
    try:
        data = await search.updateOption(item)
        insertLog.log("검색 옵션 수정 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 수정 기능 사용 실패")
        return error_list(2)

@router.post('/deleteOption')
async def OptionDelete(item: deleteOption):
    try:
        data = await search.deleteOption(item)
        insertLog.log("검색 옵션 삭제 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 삭제 기능 사용 실패")
        return error_list(2)

@router.post('/useOption')
async def OptionUsed(item: useOption, request:Request):
    if request.state.valid_token != True:
        return error_list(0)
    try:
        data = await search.useOption(item, request.state.idx)
        insertLog.log("검색 옵션 사용 등록 기능 사용")
        return {"status": 200, "data": data}
    except:
        insertLog.log("검색 옵션 사용 등록 기능 사용 실패")
        return error_list(2)
