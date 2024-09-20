from fastapi import APIRouter, Request

from utils.error_list import error_list
from .parameter import *
from .member_fn import MemberFn

router = APIRouter(
    prefix="/member",
    tags=["member"]
    )

memberFn = MemberFn()

@router.get("/getMemberList")
async def getMemberListApi(request:Request):
  if request.state.valid_token != True:
    return error_list(0)
  try:
    memberList = await memberFn.getMemberListFn(request.state.bit)
    print("memberList ::: ", memberList)
    return {"status": 200, "data": memberList}
  except Exception as e:
    print("getMemberList", e)

@router.post("/controlTrading")
async def controlTradingApi(request:Request, body:ControlAutoBody):
  if request.state.valid_token != True:
    return error_list(0)
  try:
    res = await memberFn.controlTradingFn(request.state.bit ,body.id, body.status)
    return {"status": 200, "data": res}
  except Exception as e:
    print("getMemberList", e)