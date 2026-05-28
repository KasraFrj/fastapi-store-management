from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import declarative_base
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

AsyncSessioLocal = async_sessionmaker(class_ = AsyncSession , expire_on_commit=False , bind = engine)

Base = declarative_base()

async def get_db():
    async with AsyncSessioLocal() as session:
        yield session