from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class USER_T(Base):
  __tablename__ = "nc_b_user_t"
  idx = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String(100))
  email = Column(String(100))
  password = Column(String(100))
  salt = Column(String(100))
  public_key = Column(String(100), default=None, nullable=True)
  secret_key = Column(String(100), default=None, nullable=True)
  search_option = Column(Integer, default=None, nullable=True)
  trading_option = Column(Integer, default=None, nullable=True)
  jwt_token = Column(String(100), default=None, nullable=True)
  refresh_token = Column(String(100), default=None, nullable=True)