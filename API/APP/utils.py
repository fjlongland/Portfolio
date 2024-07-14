from passlib.context import CryptContext #hashing library to hash paswords before storage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#specifying hashing algorythm for password storage

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)