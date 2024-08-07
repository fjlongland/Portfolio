from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "4u2nV" #this is insecure in practice but for now im using something basic in the future i should put a hash here
ALGORITHM = "HS256"
ACCSESS_TOKEN_EXPIRE_MINUTES = 60

#use jwt library to create tokens for user validation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCSESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, 
                             SECRET_KEY, 
                             algorithm=ALGORITHM)

    return encoded_jwt


#verify returned token to make shure user is logged in
def verify_access_token(token: str, 
                        credentials_exception):
    try:
        payload = jwt.decode(token, 
                             SECRET_KEY, 
                             algorithms=[ALGORITHM])
        
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception   
          
        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data

#this is for the depends to make shure we have a logged in user and we can access their info.
def get_current_user(token: str =  Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="could not validate credentials", 
                                         headers= {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exeption)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user