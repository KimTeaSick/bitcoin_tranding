from pydantic import BaseModel

class ControlAutoBody(BaseModel):
  id: int
  status: int