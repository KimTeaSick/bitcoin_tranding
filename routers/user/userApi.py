from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from .parameter import *
from .userFn import user_fn

userRouter = APIRouter(
    prefix= '/user',
    tags= ['user']
)

user = user_fn()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@userRouter.post('/register')
def user_register_api(item: user_register_body):
  data = user.user_register_fn(item)
  return {"status":200, "data":data}

@userRouter.post('/login')
def user_login_api(item: user_login_body):
  data = user.user_login_fn(item)
  return {"status":200, "data":data}

@userRouter.get('/getUserInfo')
def get_user_info(token:str = Depends(oauth2_scheme)):
    data = user.get_user_info_fn(token)
    return {"status":200, "data":data}

# @userRouter.get('/loginCheck')
# def user_login_check(token:str = Depends(oauth2_scheme)):
#     print("user_verfy_api", token)
#     res = user.user_login_check_fn(token)
#     return res