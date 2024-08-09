from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

password = "4u2nV@5302P"
encoded_password = urllib.parse.quote_plus(password)

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/API(tut)_DB"
#url used to connect to sql db : "postgresql://<username>:<password>@<ip-address>/<db-name>"

#creates db connection, mainly user so we can add get_db as dependency
#to enshure we are connected to a db before trying operations
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()