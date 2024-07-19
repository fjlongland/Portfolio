from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import *

router = APIRouter(
    prefix="/post",
    tags = ['posts'])#prefix allows me to remove the repitition in all the path operations


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.username)
    posts = db.query(models.Post).all()
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    return posts#in postman now displays whole array as json array

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    new_post = models.Post(**post.model_dump())#second dependecy ensures that user has been authenticated before posting

    print(current_user.username)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    return new_post#return the whole post to display on postman

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  #you can validage the input like this to make shure an int has been input(wors for all data types)
    wpost = db.query(models.Post).filter(models.Post.id == id).first()
    #print(wpost)
    #print(id)                               #make a response variable
    #wpost = findPost(id)  #calls function to find post with ID: id
    print(current_user.username)
    if wpost == None:
        print("KYS")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} was not found") #this does the same thing but better than the commented code V
        #response.status_code = status.HTTP_404_NOT_FOUND  #this is how you ste the status code to be accurate
        #return{"message": f"Post with ID: {id} was not found"}
    #else:
        #print(wpost)  
    return wpost

@router.delete("/{id}", response_model=schemas.Post) #pretty simple to delete  post at this point, especially as posts are just saved in an array
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    wpost = db.query(models.Post).filter(models.Post.id == id)
    if wpost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post was found with ID: {id}")
    print (current_user.username)
    wpost.delete()
    db.commit()
    #try:
        #cursor.execute(""" DELETE FROM posts WHERE id = %s""", (str(id)))
        #conn.commit()
    #except:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post) #Functionality for updating posts
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    upost = db.query(models.Post).filter(models.Post.id == id)

    fpost = upost.first()
    if fpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with ID:{id} was found")
    print(current_user.username)
    upost.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id))))
    #uPost = cursor.fetchone()
    #if uPost == None:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #else:
        #conn.commit()
    return upost.first()