from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/add_to_cart" , response_model=schemas.CartOut)
async def add_to_cart(item_data : schemas.CartItemCreat , db : AsyncSession = Depends(get_db) , current_user : models.User = Depends(oauth2.get_current_user)):
    product_query = select(models.product).where(models.product.id == item_data.product_id)
    result = await db.execute(product_query)
    db_product = result.scalars().first()

    if not db_product:
        raise HTTPException(status_code = 404 , detail="product now found")
    
    cart_query = select(models.Cart).where(models.Cart.user_id == current_user.id)
    result = await db.execute(cart_query)
    db_cart = result.scalars().first()

    if not db_cart:
        new_cart = models.Cart(user_id = current_user.id)
        db.add(new_cart)
        await db.commit()
        await db.refresh(new_cart)
        cart_query = select(models.Cart).where(models.Cart.id == db_cart.id).options(
    selectinload(models.Cart.items).selectinload(models.CartItem.product)
)
        cart_result = await db.execute(cart_query)
        db_cart = cart_result.scalars().first()
        
    cart_item_query = select(models.CartItem).where(models.CartItem.cart_id == db_cart.id , models.CartItem.product_id == db_product.id)
    cart_item_result = await db.execute(cart_item_query)
    cart_item = cart_item_result.scalars().first()

    if cart_item:
        cart_item.quantity += item_data.quantity
    else:
        new_cart_item = models.CartItem(cart_id = db_cart.id , product_id = db_product.id , quantity = item_data.quantity)
        db.add(new_cart_item)
    
    db_product.stock -= item_data.quantity

    await db.commit()

    final_cart_query = select(models.Cart).where(models.Cart.id == db_cart.id).options(
    selectinload(models.Cart.items).selectinload(models.CartItem.product)
)
    final_cart_result = await db.execute(final_cart_query)   
    return final_cart_result.scalars().first()



@router.get("/show_cart" , response_model=schemas.CartOut)
async def get_cart(db : AsyncSession = Depends(get_db) , current_user : models.User = Depends(oauth2.get_current_user)):
    cart_query = select(models.Cart).where(models.Cart.user_id == current_user.id)
    result = await db.execute(cart_query)
    cart = result.scalars().first()

    if not cart:
        new_cart = models.Cart(user_id = current_user.id)
        db.add(new_cart)
        await db.commit()
        await db.refresh(new_cart)
    return cart