from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel): #post class to handle validation of posts
    title: str
    content: str
    published: bool = True




@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

@app.get("/post")
def get_posts():
    return{"data": "This is your post!"}

@app.post("/createpost")
def create_post(new_post: Post):
    print(new_post.title)
    return {"data": "new post"}


#TODO : Create data base to actually store posts
