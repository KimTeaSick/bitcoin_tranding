from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from .parameter import *
from .testFn import TestFn
from fastapi import APIRouter, Request

testRouter = APIRouter(
  prefix="/test",
  tags=["test"]
)

test = TestFn()

# @testRouter.post("/cancleTrade")
# def cancleTradeApi(item: orderItem, req:Request):
#   response = test.cancleTradeFn(item, req.state.bit)
#   return response

@testRouter.post("/signTrade")
def signTradeApi(item: orderItem, req:Request):
  response = test.signTradeFn(item, req.state.bit)
  return response

@testRouter.get("/cancleTrade")
def signTradeApi(req:Request):
  response = test.cancleTradeFn()
  return response