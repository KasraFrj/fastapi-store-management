from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/add_to_cart" , response_model=schemas.CartOut)
def add_to_cart(item_data : schemas.CartItemCreat , db : Session = Depends(get_db) , current_user : models.User = Depends(oauth2.get_current_user)):
    db_product = db.query(models.product).filter(models.product.id == item_data.product_id).first()

    if not db_product:
        raise HTTPException(status_code = 404 , detail="product now found")
    
    db_cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not db_cart:
        new_cart = models.Cart(user_id = current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)

    cart_item = db.query(models.CartItem).filter(models.CartItem.cart_id == db_cart.id , models.CartItem.product_id == db_product.id).first()

    if cart_item:
        cart_item.quantity += item_data.quantity
    else:
        new_cart_item = models.CartItem(cart_id = db_cart.id , product_id = db_product.id , quantity = item_data.quantity)
        db.add(new_cart_item)

    db.commit()
    db.refresh(cart_item)
    return db_cart

@router.get("/show_cart" , response_model=schemas.CartOut)
def get_cart(db : Session = Depends(get_db) , current_user : models.User = Depends(oauth2.get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        new_cart = models.Cart(user_id = current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
    return cart