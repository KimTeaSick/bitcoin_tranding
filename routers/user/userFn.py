from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from sqlalchemy.orm import Session
from database import SessionLocal
from lib.makeSalt import make_salt
import hashlib
from .models import *

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class user_fn():

  def user_register_fn(self, item):
    try:
      user_t_check = db.query(USER_T).filter(USER_T.email == item.email).first()
      if user_t_check != None: return 333

      user_name = item.name
      user_email = item.email
      user_pw = item.password
      user_public = item.public
      user_secret = item.secret
      salt = make_salt()
      
      after_hash_pw = hashlib.sha256((user_pw + salt).encode()).hexdigest()
      after_hash_public = hashlib.sha256((user_public + salt).encode()).hexdigest()
      after_hash_secret = hashlib.sha256((user_secret + salt).encode()).hexdigest()
      user_table = USER_T()
      user_table.name = user_name
      user_table.password = after_hash_pw
      user_table.email = user_email
      user_table.salt = salt
      user_table.public_key = after_hash_public
      user_table.secret_key = after_hash_secret
      db.add(user_table)
      db.commit()
      return 200
    except Exception as e:
      print("Error", e)
      return 444
    
  def user_login_fn(self, item):
    user_info = db.query(USER_T).filter(USER_T.email == item.email).first()
    user_password = user_info.password
    user_salt = user_info.salt

    enter_password = hashlib.sha256((item.password + user_salt).encode())
    enter_password = enter_password.hexdigest()

    if(enter_password == user_password):
      return { "status" : 200, "data":{ "idx":user_info.idx ,"name": user_info.name } }
    else : 
      return { "status" : 444 }
