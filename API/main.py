from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: int



#add an array of posts jus for testing while i dont have a database yet
my_posts =[{"title": "Title of post 1", "content": "Content of post 1", "published": True, "rating": 1, "id": 11111}, 
           {"title": "Title of post 2", "content": "Content of post 2", "published": False, "rating": None, "id": 11112}]

@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

@app.get("/post")
def get_posts():
    return{"data": my_posts}#in postman now displays whole array as json array

@app.post("/post")
def create_post(post: Post):
    print(post.model_dump())#prints new post to consol asa dictionary
    my_posts.append(post.model_dump())#adds new post to array
    print("////////////////////////////////////////")
    print(post)#only prints infro from new post in consol
    return {"data": post}#return the whole post to display on postman


#TODO : Create data base to actually store posts
#TODO : make shure the post ID are always unique
