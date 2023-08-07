from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
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
  res = user.user_register_fn(item)
  return res

@userRouter.post('/login')
def user_login_api(item: user_login_body):
  res = user.user_login_fn(item)
  print(res)
  return {"access_token": res[1], "token_type": "bearer"}

@userRouter.get('/verify')
def user_verfy_api(token:str = Depends(oauth2_scheme)):
    print("user_verfy_api", token)
    res = user.verfy_token(token)
    return res

@userRouter.get('/loginCheck')
def user_login_check(token:str = Depends(oauth2_scheme)):
    print("user_verfy_api", token)
    res = user.user_login_check(token)
    return res