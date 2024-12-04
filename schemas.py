from typing import List
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    
class BlogBase(Blog):
    class Config():
        orm_mode = True
    
        
class User(BaseModel):
    name: str
    email: str
    password: str
    
    

class UserData(BaseModel):
    name: str 
    email: str
    # blogs: List[BlogBase] = []
    class Config():
        orm_mode = True




class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserData
    
    
    class Config:
        orm_mode = True
        

class Login(BaseModel):
    username: str
    password: str  
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
        