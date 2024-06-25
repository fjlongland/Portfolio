from fastapi import FastAPI, Response, status, HTTPException
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

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, response: Response):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 999999999)
    print(post_dict["id"])
    my_posts.append(post_dict)
    return {"data": post_dict}#return the whole post to display on postman



@app.get("/post/{id}")
def get_post(id: int, response: Response):  #you can validage the input like this to make shure an int has been input(wors for all data types)
    print(id)                               #make a response variable
    wpost = findPost(id)  #calls function to find post with ID: id
    if wpost == None:
        print("KYS")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} was not found") #this does the same thing but better than the commented code V
        #response.status_code = status.HTTP_404_NOT_FOUND  #this is how you ste the status code to be accurate
        #return{"message": f"Post with ID: {id} was not found"}
    else:
        print(wpost)  
    return{"post": wpost}


#TODO : Create data base to actually store posts

