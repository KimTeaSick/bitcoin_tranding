from typing import Optional
from pydantic import BaseModel

class updateDisparityOptionBody(BaseModel):
  line_one: dict
  line_two: dict
  line_three: dict

class getAvgDataBody(BaseModel):
  range: int
  coin: str
  term: str