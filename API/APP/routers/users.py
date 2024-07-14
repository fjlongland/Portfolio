from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import *


router = APIRouter(
    prefix="/users",
    tags = ['users'])#prefix allows me to remove the repitition in all the path operations

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # HASH THE PASSWORD - User.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #cursor.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING *""", (user.username, user.password, user.email))
    #new_user = cursor.fetchone()
    #conn.commit()
    return new_user

@router.get("/", response_model= List[schemas.User])
def show_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    #cursor.execute("""SELECT * FROM users ORDER BY id ASC""")
    #aUsers = cursor.fetchall()
    return users

@router.get("/{id}", response_model=schemas.User)
def show_one_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        #cursor.execute("""SELECT * FROM users WHERE id = %s""", str(id))
        #wUser = cursor.fetchone()
    except:
        user = None

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with ID: {id}")
    else:
        return user

@router.put("/{id}", response_model=schemas.User)
def update_user(user: schemas.UserCreate, id: int, db: Session = Depends(get_db)):
    nUser = db.query(models.User).filter(models.User.id == id)

    fUser = nUser.first()
    #cursor.execute("""UPDATE users SET username = %s, Password = %s, email = %s WHERE id = %s RETURNING *""", (user.username, user.password, user.email, str(id)))
    #nUser = cursor.fetchone()
    #conn.commit()
    if fUser == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with ID: {id}")
    
    nUser.update(user.model_dump(), synchronize_session=False)
    db.commit()
    
    return nUser.first()

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    dUser = db.query(models.User).filter(models.User.id == id)

    if dUser.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    dUser.delete()
    db.commit()
    #try:
        #cursor.execute("""DELETE FROM users WHERE id = %s""", str(id))
        #conn.commit()
    #except:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)