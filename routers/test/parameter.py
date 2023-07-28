from pydantic import BaseModel

class orderItem(BaseModel):
  type: str
  order_id:str
  coin: str
