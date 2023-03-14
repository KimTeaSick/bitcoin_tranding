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

class getAvgData(BaseModel):
  range: int
  coin: str
  term: str