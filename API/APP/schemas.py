from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel): #response model for users
    username: str
    email: str
    id: int

    class Config:
        orm_model = True

class Post(PostBase): #this class defines the response model for the postst that are returned in the appication
    id: int
    created_at: datetime
    user_id_fk: int
    owner: User

    class Config:
        orm_model = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None