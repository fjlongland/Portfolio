from passlib.context import CryptContext #hashing library to hash paswords before storage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#specifying hashing algorythm for password storage

def hash(password: str):# Hashes password for user security
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):#$validates user when needed
    return pwd_context.verify(plain_password, 
                              hashed_password)