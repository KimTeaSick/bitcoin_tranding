<<<<<<< HEAD
from routers.user.userApi import user
=======
from routers.user.user_api import user
>>>>>>> bd85bc4b6ee51082127d8c6ceea798faa4ed4c0a
from platformPrivate import BitThumbPrivate
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import jwt

SECRET = "randomstring"

async def token_validator(request):
  try:
    db = SessionLocal()
    db: Session
    headers = request.headers
    decode_token = jwt.decode(headers.get("authorization").replace("Bearer ", ""), SECRET, algorithms="HS256", verify=True)
    user_info = db.query(models.USER_T).filter(models.USER_T.idx == decode_token["idx"]).first()
    idx = decode_token["idx"]
    bit = BitThumbPrivate(user_info.public_key, user_info.secret_key)
    return bit, idx
  except Exception as e:
    print("token_validator Error", e)
    db.rollback()
    return 401
  finally:
    db.close()