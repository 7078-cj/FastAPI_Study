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
        
class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    
    class Config:
        orm_mode = True 
        
class CreateUserRequest(BaseModel):
    
    username: str
    password: str
    
class Token(BaseModel):
    
    access_token: str
    token_type: str
    
 

    
    