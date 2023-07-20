from typing import Optional
from pydantic import BaseModel

class tradingOption(BaseModel):
    name: str
    account: dict
    buy: dict
    sell: dict

class getTradingOptionDetail(BaseModel):
    name: str

class deleteTradingOption(BaseModel):
    name: str

class useTradingOption(BaseModel):
    name: str

    
class controlAT(BaseModel):
    flag: int