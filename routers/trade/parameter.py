from typing import Optional
from pydantic import BaseModel

class insetTradingOption(BaseModel):
    name: str
    account: dict
    buy: dict
    sell: dict

class tradingOption(insetTradingOption):
    idx: int

class getTradingOptionDetail(BaseModel):
    idx: int

class deleteTradingOption(BaseModel):
    idx: int

class useTradingOption(BaseModel):
    idx: int

class controlAT(BaseModel):
    flag: int

class sellInfoBody(BaseModel):
    coin: str
    sellType: int
    sellPrice: float
    coinUnit: float
    cancleTime: int