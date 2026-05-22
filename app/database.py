from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SessioLocal = sessionmaker(autocommit = False , autoflush=False , bind = engine)

Base = declarative_base()

def get_db():
    db = SessioLocal()
    try:
        yield db
    finally:
        db.close()