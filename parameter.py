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

class getRecommendOption(BaseModel):
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Disparity: dict
    Trend: dict
    MACD: dict

class getSearchOptionBody(BaseModel):  
  name:str
  price: str
  trends_term: str
  trends: str
  avg_volume: str
  first_disparity: str
  second_disparity: str
  transaction_amount: str

class updateSearchOptionBody(getSearchOptionBody):
  idx: int

class updateDisparityOptionBody(BaseModel):
  line_one: dict
  line_two: dict
  line_three: dict
  
class updateUseSearchOptionBody(BaseModel):
  num: str

class insertOption(BaseModel):
    Name: str
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Disparity: dict
    Trend: dict
    MACD: dict

class getOptionDetail(BaseModel):  
  option: str

class updateOption(BaseModel):  
    Name: str
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Disparity: dict
    Trend: dict
    MACD: dict

class deleteOption(BaseModel):  
  option: str

class useOption(BaseModel):  
  option: str
