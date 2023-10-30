
from typing import Optional
from pydantic import BaseModel

class GetCandleStickBody(BaseModel):
    id:  Optional[str] = None
    term: Optional[str] = None

class BuyAndSell(BaseModel):
    coin: str
    price: str
    unit: str

class getDateOrderListBody(BaseModel):
    date: list
    page: str

class getAccountInfoBody(BaseModel):
    date: list

class newSearchBody(BaseModel):
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Trend: dict
    Disparity: dict
    MACD: dict

class getSearchOptionBody(BaseModel):
    name: str
    price: str
    trends_term: str
    trends: str
    avg_volume: str
    first_disparity: str
    second_disparity: str
    transaction_amount: str

class updateSearchOptionBody(getSearchOptionBody):
    idx: int

class updateUseSearchOptionBody(BaseModel):
    num: str

class searchOptionBody(BaseModel):
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Disparity: dict
    Trend: dict
    MACD: dict