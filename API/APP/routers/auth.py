from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    tags=['Autentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "invalid credentials")

    return {"token": "example token"}