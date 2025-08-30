from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True 


    
    