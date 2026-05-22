from pydantic import BaseModel , EmailStr

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int 
    email : EmailStr
    is_admin :bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None

class ProductCreate(BaseModel):
    title: str
    description: str | None = None
    price: int
    stock: int

class ProductOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: int
    stock: int

    class Config:
        from_attributes = True


class CartItemCreat(BaseModel):
    product_id : int
    quantity : int = 1

class CartItemOut(BaseModel):
    id : int
    product_id : int
    quantity : int
    product : ProductOut

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id : int
    user_id : int
    items : list[CartItemOut] = []

    class Config:
        from_attributes = True