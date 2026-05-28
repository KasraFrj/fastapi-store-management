from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from app import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeyxyz123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def get_current_user(token : str = Depends(oauth2_scheme) , db : AsyncSession = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="توکن نامعتبر است یا منقضی شده است.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    user_query = select(models.User).where(models.User.id == user_id)
    result = await db.execute(user_query)
    if result is None:
        return credentials_exception
    
    return result.scalars().first()