from pydantic import BaseModel

class user_register_body(BaseModel):
  name: str
  email: str
  phone: str
  password: str
  public: str
  secret: str
  platform: str

class user_login_body(BaseModel):
  email: str
  password: str
