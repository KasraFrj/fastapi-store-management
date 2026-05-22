from .. import models , utils , schemas
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth" , tags=["Authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/signup" , response_model=schemas.UserOut)
def signup(user : schemas.UserCreate , db : Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400 , detail="Email already Exist")
    
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(email = user.email , hashed_password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not db_user:
        raise HTTPException(status_code=403 , detail="Wrong Email")
    
    if not utils.verify_password(user_credentials.password , db_user.hashed_password):
        raise HTTPException(status_code=403 , detail="Wrong Password")
    
    access_token = utils.create_access_token(data={"user_id" : db_user.id})

    return {"access_token" : access_token , "type_token" : "bearer"}