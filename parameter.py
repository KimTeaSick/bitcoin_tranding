from typing import Optional
from pydantic import BaseModel


class GetCandleStickBody(BaseModel):
  id:  Optional[str] = None
  term: Optional[str] = None

class BuyAndSell(BaseModel):
  coin: str
  unit: str

class getOrderListBody(BaseModel):
  page: str

class getAvgDataBody(BaseModel):
  range: int
  coin: str
  term: str

class getDateOrderListBody(BaseModel):
  date: list
  page: str

class getAccountInfoBody(BaseModel):
  date: list

class getSearchOptionBody(BaseModel):  
  name:str
  price: str
  trends: str
  avg_volume: str
  first_disparity: str
  second_disparity: str
  transaction_amount: str
