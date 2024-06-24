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



#add an array of posts jus for testing while i dont have a database yet
my_posts =[{"title": "Title of post 1", "content": "Content of post 1", "published": True, "rating": 1, "id": 11111}, 
           {"title": "Title of post 2", "content": "Content of post 2", "published": False, "rating": None, "id": 11112}]


def findPost(id):  # simple for loop to find post with ID: id 
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

@app.get("/post")
def get_posts():
    return{"data": my_posts}#in postman now displays whole array as json array

@app.post("/post")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 999999999)
    print(post_dict["id"])
    my_posts.append(post_dict)
    return {"data": post_dict}#return the whole post to display on postman



@app.get("/post/{id}")
def get_post(id: int):  #you can validage the input like this to make shure an int has been input(wors for all data types)
    print(id)
    wpost = findPost(id)  #calls function to find post with ID: id
    print(wpost)  
    return{"post": wpost}


#TODO : Create data base to actually store posts

