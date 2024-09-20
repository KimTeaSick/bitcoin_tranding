from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from .parameter import *
from .user_fn import user_fn

router = APIRouter(
    prefix= '/user',
    tags= ['user']
)

user = user_fn()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/register')
def user_register_api(item: user_register_body):
  data = user.user_register_fn(item)
  return {"status":200, "data":data}

@router.post('/login')
def user_login_api(item: user_login_body):
  data = user.user_login_fn(item)
  return {"status":200, "data":data}

@router.get('/getUserInfo')
def get_user_info(token:str = Depends(oauth2_scheme)):
    data = user.get_user_info_fn(token)
    return {"status":200, "data":data}