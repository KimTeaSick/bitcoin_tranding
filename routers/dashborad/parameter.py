from typing import Optional
from pydantic import BaseModel

class getRecommendOption(BaseModel):
  Price: dict
  TransactionAmount: dict
  MASP: dict
  Trend: dict
  Disparity: dict
  MACD: dict

class rateCheckBody(BaseModel):
  days: int

class getPcoinInfoBody(BaseModel):
  idx: int