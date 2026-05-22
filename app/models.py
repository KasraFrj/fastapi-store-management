from app.database import Base
from sqlalchemy import Integer , String , Boolean , Text , Column , ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key = True , index = True)
    email = Column(String , unique=True , nullable=False , index=True)
    hashed_password = Column(String , nullable=False)
    is_admin = Column(Boolean , default=False)

class product(Base):
    __tablename__ = "products"

    id = Column(Integer , primary_key=True , index=True)
    title = Column(String , nullable=False , index=True)
    description = Column(Text , nullable=True)
    price = Column(Integer , nullable=False)
    stock = Column(Integer , default=0)


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer , primary_key=True , nullable=False)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    items = relationship("CartItem" , back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer , primary_key=True , nullable=False)
    cart_id = Column(Integer , ForeignKey("carts.id") , nullable=False)
    product_id = Column(Integer , ForeignKey("products.id") , nullable=False)
    quantity = Column(Integer , default=1 , nullable=False)

    cart = relationship("Cart" , back_populates="items")
    product = relationship("product")