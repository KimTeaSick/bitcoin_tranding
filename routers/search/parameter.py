from typing import Optional
from pydantic import BaseModel

class insertOption(BaseModel):
    Name: str
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Trend: dict
    Disparity: dict
    MACD: dict

class getOptionDetail(BaseModel):
    option: int

class updateOption(BaseModel):
    idx: int
    Name: str
    Price: dict
    TransactionAmount: dict
    MASP: dict
    Trend: dict
    Disparity: dict
    MACD: dict
    
class deleteOption(BaseModel):
    option: str

class useOption(BaseModel):
    option: str
