from typing import Optional
from pydantic import BaseModel

class tradingOption(BaseModel):
    name: str
    account: dict
    buy: dict
    sell: dict
    idx: int

class getTradingOptionDetail(BaseModel):
    idx: int

class deleteTradingOption(BaseModel):
    idx: int

class useTradingOption(BaseModel):
    idx: int

class controlAT(BaseModel):
    flag: int