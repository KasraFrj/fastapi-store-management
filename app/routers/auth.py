from .. import models , utils , schemas
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth" , tags=["Authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup" , response_model=schemas.UserOut)
async def signup(user : schemas.UserCreate , db : AsyncSession = Depends(get_db)):

    query = select(models.User).where(models.User.email == user.email)
    result = await db.execute(query)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=400 , detail="Email already Exist")
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(email = user.email , hashed_password = hashed_pwd)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db : AsyncSession = Depends(get_db)):

    query = select(models.User).where(models.User.email == user_credentials.username)
    result = await db.execute(query)
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=403 , detail="Wrong Email")
    
    if not utils.verify_password(user_credentials.password , db_user.hashed_password):
        raise HTTPException(status_code=403 , detail="Wrong Password")
    
    access_token = utils.create_access_token(data={"user_id" : db_user.id})

    return {"access_token" : access_token , "token_type" : "bearer"}