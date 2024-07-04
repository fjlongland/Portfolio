from pydantic import BaseModel


class Post(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class User(BaseModel):
    username: str
    password: str
    email: str