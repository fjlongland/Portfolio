from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase): #this class defines the response model for the postst that are returned in the appication
    id: int
    created_at: datetime


    class Config:
        orm_model = True

class User(BaseModel):
    username: str
    password: str
    email: str
    