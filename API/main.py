from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None




@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

@app.get("/post")
def get_posts():
    return{"data": "This is your post!"}

@app.post("/createpost")
def create_post(post: Post):
    print(post.dict())#prints new post to consol asa dictionary
    print("////////////////////////////////////////")
    print(post)#only prints infro from new post in consol
    return {"data": post}#return the whole post to display on postman


#TODO : Create data base to actually store posts
