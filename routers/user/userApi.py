from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from lib.pagiNation import PagiNation
from fastapi import APIRouter
from .parameter import *
from .userFn import user_fn

userRouter = APIRouter(
    prefix= '/user',
    tags= ['user']
)

user = user_fn()

@userRouter.post('/register')
def user_register_api(item: user_register_body):
  res = user.user_register_fn(item)
  return res

@userRouter.post('/login')
def user_login_api(item: user_login_body):
  res = user.user_login_fn(item)
  return res