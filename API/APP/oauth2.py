from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "4u2nV" #this is insecure in practice but for now im using something basic in the future i should put a hash here
ALGORITHM = "HS256"
ACCSESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCSESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
