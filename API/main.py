from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

@app.get("/post")
def get_posts():
    return{"data": "This is your post!"}

@app.post("/createpost")
def create_post(payLoad: dict = Body):
    print(payLoad)
    return{"new-post": f"Title: {payLoad['Title']}; Content: {payLoad['Content']}"}#function to create a post, post details made in postman

#TODO : Create data base to actually store posts
