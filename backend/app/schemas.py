from pydantic import BaseModel
from typing import List, Optional

class Fruit(BaseModel):
    id: int| None = None
    name: str
    
    class Config:
        orm_mode = True 
        
class FruitUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    
    class Config:
        orm_mode = True 


    
    