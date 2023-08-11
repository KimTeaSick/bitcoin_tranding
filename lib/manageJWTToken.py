from datetime import datetime, timedelta
import jwt

SECRET = "randomstring"
access_expiration_time = 180
refresh_expiration_time = 3

def make_access_JWT_token(data):
  now = datetime.utcnow()
  token_expiration_time = now + timedelta( days = access_expiration_time )
  data["exp"] = token_expiration_time
  token = jwt.encode( data, SECRET, algorithm="HS256" )
  return token

def make_refresh_JWT_token():
  now = str(datetime.utcnow())
  token_expiration_time = now + timedelta( hours = refresh_expiration_time )
  token = jwt.encode({"exp": token_expiration_time}, SECRET, algorithm="HS256")
  return token

def verify_jwt_token(token):
  try:
    jwt.decode(token, SECRET, algorithms="HS256", verify=True)
    return 200
  except Exception as e:
    print("verify_jwt_token ::: :::", e)
    return 333
  