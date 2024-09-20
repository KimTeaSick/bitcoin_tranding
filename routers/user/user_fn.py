from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/4season/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
import hashlib
import models
import jwt
from pyupbit import Upbit
from pybithumb import Bithumb
from database import SessionLocal
from sqlalchemy.orm import Session
from utils.makeSalt import make_salt
from BitThumbPrivate import BitThumbPrivate
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from utils.manageJWTToken import make_access_JWT_token, verify_jwt_token

SECRET = "randomstring"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class user_fn():
  def __init__(self):
    self.bithumb = None
    self.user_idx = None

  def user_register_fn(self, item):
    try:
      user_t_check = db.query(models.USER_T).filter(models.USER_T.email == item.email).first()
      if user_t_check != None: return 333
      if item.platform == '1':
        bit = Bithumb(item.public, item.secret)
        pass_registe = bit.get_balance('ALL')
        if pass_registe['status'] != '0000': return 456
      elif item.platform == '2':
        bit = Upbit(item.public, item.secret)
        pass_registe = bit.get_balances()
        if len(pass_registe) < 1: return 456
      user_name = item.name
      user_email = item.email
      user_phone = item.phone
      user_pw = item.password
      user_public = item.public
      user_secret = item.secret
      user_platform = item.platform

      salt = make_salt()
      after_hash_pw = hashlib.sha256((user_pw + salt).encode()).hexdigest()

      user_table = models.USER_T()
      user_table.name = user_name
      user_table.password = after_hash_pw
      user_table.email = user_email
      user_table.phone = user_phone
      user_table.platform = user_platform
      user_table.salt = salt
      user_table.public_key = user_public
      user_table.secret_key = user_secret
      user_table.active = 0

      db.add(user_table)
      db.commit()
      return 200
    except Exception as e:
      print("Error", e)
      db.rollback()
      return 444
    
  def user_login_fn(self, item):
    try:
      db = SessionLocal()
      db: Session
      user_info = db.query(models.USER_T).filter(models.USER_T.email == item.email).first()
      print("user_login_fn start!", user_info)
      user_password = user_info.password
      user_salt = user_info.salt
      enter_password = hashlib.sha256((item.password + user_salt).encode())
      enter_password = enter_password.hexdigest()
      print("user_login_fn start!!")
      if(enter_password == user_password):
        token = make_access_JWT_token({"idx":user_info.idx, "email":user_info.email, "name":user_info.name, "platform":user_info.platform })
        user_info.jwt_token = token
        user_info.refresh_token = token
        self.user_idx = user_info.idx
        self.bithumb = BitThumbPrivate(user_info.public_key, user_info.secret_key)
        db.add(user_info)
        db.commit()
        return {"status":200, "data": {
          "idx":user_info.idx,
          "name": user_info.name, 
          "platform":user_info.platform,
          "auto_active": user_info.active,
          "access_token": token, 
          "token_type": "bearer"
          }}
      
      else : 
        return { "status" : 444 }
    except Exception as e:
      print("Error", e)
      db.rollback()
    finally:
      db.close()

  def user_login_check_fn(self, token):
    try:
      token_boolean = verify_jwt_token(token)
      if token_boolean == 200:
        user_info = db.query(models.USER_T).filter(models.USER_T.jwt_token == token).first()
        return BitThumbPrivate(user_info.public_key, user_info.secret_key)
      else:
        return 444
    except Exception as e:
      print("verfy_token Error ::: :::", e)
      db.rollback()
      return 333
    
  def get_user_info_fn(self, token):
    try:
      token_boolean = verify_jwt_token(token)
      if token_boolean == 200: 
        userInfo = self.get_user_info(token)
        return userInfo
      else:
        return 444
    except Exception as e:
      print("verfy_token Error ::: :::", e)
      db.rollback()
      return 333
    
  def get_user_info(self, token):
    user = db.query(models.USER_T).filter(models.USER_T.jwt_token == token).first()
    idx = user.idx
    name = user.name
    email = user.email
    return {"idx":idx, "name":name, "email":email}

  def connect_bithumb_privit(self, token):
    try:
      decode_token = jwt.decode(token, SECRET, algorithms="HS256", verify=True)
      print("decode_token ::: ::: ", decode_token)
      user_info = db.query(models.USER_T).filter(models.USER_T.idx == decode_token["idx"]).first()
      idx = decode_token["idx"]
      bit = BitThumbPrivate(user_info.public_key, user_info.secret_key)
      return bit, idx
    except Exception as e:
      print("connect_bithumb_privit Error", e)
      db.rollback()
      return 456