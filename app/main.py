from fastapi import FastAPI , HTTPException , Depends
from app import models
from app.database import engine , Base
from app.routers import auth , products , cart
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#models.Base.metadata.create_all(bind = engine)

app = FastAPI(title="E-Commerce API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)

@app.get("/hello")
def say_hi():
    return {"message" : "Hello World"}

@app.get("/users/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token, "message": "شما احراز هویت شده‌اید!"}