from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2;
from psycopg2.extras import RealDictCursor
import time
import email_validator
from sqlalchemy.orm import Session
from . import schemas, models
from .database import *

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
        conn = psycopg2.connect(host = 'localhost', dbname = 'API(tut)_DB', user = 'postgres', password = '4u2nV@5302P', cursor_factory=RealDictCursor)
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
#def findPost(id):  # simple for loop to find post with ID: id 
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


@app.get("/post", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    return posts#in postman now displays whole array as json array

@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    return new_post#return the whole post to display on postman

@app.get("/post/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):  #you can validage the input like this to make shure an int has been input(wors for all data types)
    wpost = db.query(models.Post).filter(models.Post.id == id).first()
    #print(wpost)
    #print(id)                               #make a response variable
    #wpost = findPost(id)  #calls function to find post with ID: id
    if wpost == None:
        print("KYS")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} was not found") #this does the same thing but better than the commented code V
        #response.status_code = status.HTTP_404_NOT_FOUND  #this is how you ste the status code to be accurate
        #return{"message": f"Post with ID: {id} was not found"}
    #else:
        #print(wpost)  
    return wpost

@app.delete("/post/{id}", response_model=schemas.Post) #pretty simple to delete  post at this point, especially as posts are just saved in an array
def delete_post(id: int, db: Session = Depends(get_db)):
    wpost = db.query(models.Post).filter(models.Post.id == id)
    if wpost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post was found with ID: {id}")
    
    wpost.delete()
    db.commit()
    #try:
        #cursor.execute(""" DELETE FROM posts WHERE id = %s""", (str(id)))
        #conn.commit()
    #except:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}", response_model=schemas.Post) #Functionality for updating posts
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    upost = db.query(models.Post).filter(models.Post.id == id)

    fpost = upost.first()
    if fpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with ID:{id} was found")
    
    upost.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    #uPost = cursor.fetchone()
    #if uPost == None:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #else:
        #conn.commit()
    return upost.first()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, response: Response):
    cursor.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING *""", (user.username, user.password, user.email))
    new_user = cursor.fetchone()
    conn.commit()
    return{"Data": new_user}

@app.get("/users")
def show_all_users():
    cursor.execute("""SELECT * FROM users ORDER BY id ASC""")
    aUsers = cursor.fetchall()
    return{"data": aUsers}

@app.get("/users/{id}")
def show_one_user(id: int):
    try:
        cursor.execute("""SELECT * FROM users WHERE id = %s""", str(id))
        wUser = cursor.fetchone()
    except:
        wUser = None

    if wUser == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with ID: {id}")
    else:
        return{"Data": wUser}

@app.put("/users/{id}")
def update_user(user: schemas.UserCreate, id: int):
    cursor.execute("""UPDATE users SET username = %s, Password = %s, email = %s WHERE id = %s RETURNING *""", (user.username, user.password, user.email, str(id)))
    nUser = cursor.fetchone()
    conn.commit()
    if nUser == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with ID: {id}")
    return{"Data": nUser}

@app.delete("/users/{id}")
def delete_user(id: int):
    try:
        cursor.execute("""DELETE FROM users WHERE id = %s""", str(id))
        conn.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#///////////////////////////////  NOTES  //////////////////////////////////////////////////////////

#uvicorn API.APP.main:app --reload

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
