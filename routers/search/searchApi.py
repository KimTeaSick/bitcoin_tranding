import sys
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back")

from fastapi import APIRouter
from .parameter import *
from .searchFn import SearchFn
from lib import insertLog

searchRouter = APIRouter(
    prefix="/option",
    tags=["option"]
)

search = SearchFn()

@searchRouter.post('/insertOption')
async def updateSearchOption(item: insertOption):
    try:
        response = await search.insertOption(item)
        insertLog.log("검색 옵션 등록 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 등록 기능 사용 실패")

@searchRouter.get('/optionList')
async def getOptionList():
    try:
        response = await search.optionList()
        insertLog.log("검색 옵션 조회 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 조회 기능 사용 실패")
        return 444

@searchRouter.post('/optionDetail')
async def selectOptionDetail(item: getOptionDetail):
    try:
        print("item",item)
        response = await search.optionDetail(item)
        insertLog.log("검색 옵션 상세 조회 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 상세 조회 기능 사용 실패")
        return 444

@searchRouter.post('/updateOption')
async def UpdateOption(item: updateOption):
    try:
        response = await search.updateOption(item)
        insertLog.log("검색 옵션 수정 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 수정 기능 사용 실패")
        return 444

@searchRouter.post('/deleteOption')
async def OptionDelete(item: deleteOption):
    try:
        response = await search.deleteOption(item)
        insertLog.log("검색 옵션 삭제 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 삭제 기능 사용 실패")
        return 444

@searchRouter.post('/useOption')
async def OptionUsed(item: useOption):
    try:
        response = await search.useOption(item)
        insertLog.log("검색 옵션 사용 등록 기능 사용")
        return response
    except:
        insertLog.log("검색 옵션 사용 등록 기능 사용 실패")
        return 444
