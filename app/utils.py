from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone
import jwt

pwd_context = CryptContext(schemes = ["bcrypt"] , deprecated = "auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(plain_password : str , hashed_password : str):
    return pwd_context.verify(plain_password , hashed_password)

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encode_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm = ALGORITHM)

    return encode_jwt