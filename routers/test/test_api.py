from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from .parameter import *
from .test_fn import TestFn
from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/test",
  tags=["test"]
)

test = TestFn()

# @router.post("/cancleTrade")
# def cancleTradeApi(item: orderItem, req:Request):
#   response = test.cancleTradeFn(item, req.state.bit)
#   return response

@router.post("/signTrade")
def signTradeApi(item: orderItem, req:Request):
  response = test.signTradeFn(item)
  return response

@router.get("/test")
def testApi():
  response = test.testFn()
  return response

@router.get("/cancleTrade")
def signTradeApi(req:Request):
  response = test.cancleTradeFn()
  return response