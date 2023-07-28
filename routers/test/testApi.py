from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from .parameter import *
from .testFn import TestFn
from fastapi import APIRouter

testRouter = APIRouter(
  prefix="/test",
  tags=["test"]
)

test = TestFn()

@testRouter.post("/cancleTrade")
def cancleTradeApi(item: orderItem):
  response = test.cancleTradeFn(item)
  return response

@testRouter.post("/signTrade")
def signTradeApi(item: orderItem):
  response = test.signTradeFn(item)
  return response