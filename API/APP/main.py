from fastapi import FastAPI, Depends
import psycopg2;
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import *
from .routers import post, users, auth

#/////////////////////////////////////////////////////////////////////////////
#///Full documentation generated by fastAPI at : http://127.0.0.1:8000/docs///
#/////////////////////////////////////////////////////////////////////////////
#use http://127.0.0.1:8000/redoc for a reformatted version of this documentation

#///////////////////////////  STUFF  ////////////////////////////////////////////////////////////

models.Base.metadata.create_all(bind=engine)#creates a DB table if there isnt one already

app = FastAPI()

#used this to test some stuff
@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return{'data': posts}

#///////////////  DATABASE CONNECTION /////////////////////////////////////////////////////////////////////
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', 
                                dbname = 'API(tut)_DB', 
                                user = 'postgres', 
                                password = '4u2nV@5302P', 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection Successful!")
        break
    except Exception as error:
        print("Connection Failed, Too Bad")
        print("Error: ", error)
        time.sleep(2)

#add an array of posts jus for testing while i dont have a database yet
#my_posts =[{"title": "Title of post 1", "content": "Content of post 1", "published": True, "rating": 1, "id": 11111}, 
#           {"title": "Title of post 2", "content": "Content of post 2", "published": False, "rating": None, "id": 11112}]

#///////////////////////////// FUNCTIONS ///////////////////////////////////////////////////////////////////////////
#this function was used when i was still using an array to store my posts
#def findPost(id)s:  # simple for loop to find post with ID: id 
    #try:
        #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))   
        #p = cursor.fetchone()
    #except:
        #p = None
    #return p

#def findIndex(id):     # function to delete a post when given a specific post ID
    #for i, p in enumerate(my_posts): #this functionality wil change when we start saving posts in an actual databaase
        #if p["id"] == id:
            #return i
        
#/////////////////////////////  OPERATIONS  ///////////////////////////////////////////////////////////////////

@app.get("/") #decorator references app(instance of fats API you are using) and specifys file path to the changes you are making
async def root(): #init the function and specify its name
    return{"message:" "Hi There trveler!"} #code that runs in the function and makes changes at specified destiantion

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

app.include_router(post.router)#routs all http requestsfor /post to the post directory
app.include_router(users.router)#routs all HTTP requests for / users to the users directory
app.include_router(auth.router)

#///////////////////////////////  NOTES  //////////////////////////////////////////////////////////

#uvicorn API.APP.main:app --reload

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
