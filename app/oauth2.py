from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
import os
from app import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeyxyz123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="توکن نامعتبر است یا منقضی شده است.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id)
    if user is None:
        return credentials_exception
    
    return user.first()