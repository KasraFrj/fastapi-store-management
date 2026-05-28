from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete , update
from sqlalchemy.future import select
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/products" , tags=["Products"])

@router.post("/create" , response_model=schemas.ProductOut)
async def create_product(product_data : schemas.ProductCreate , db : AsyncSession = Depends(get_db)):
    new_product = models.product(**product_data.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/read_product" , response_model=List[schemas.ProductOut])
async def read_product(db : AsyncSession = Depends(get_db)):
    query = select(models.product)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

@router.get("/read_product/{id}" , response_model=schemas.ProductOut)
async def get_one_product(id : str , db : AsyncSession = Depends(get_db)):
    query = select(models.product).where(models.product.id == id)
    result = await  db.execute(query)
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code = 404 , detail=f" {id} Not Found")
    return db_product

@router.delete("/delete/{id}")
async def delete_product(id : int , db : AsyncSession = Depends(get_db)):
    query = select(models.product).where(models.product.id == id)
    result = await db.execute(query)
    product = result.scalars().first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"محصولی با شناسه {id} برای حذف یافت نشد."
        )
    
    delete_query = delete(models.product).where(models.product.id == id)
    await db.execute(delete_query)
    await db.commit()
    return {"message": "محصول با موفقیت حذف شد."}

@router.put("/update/{id}" , response_model=schemas.ProductOut)
async def update_product(id : int , new_data : schemas.ProductCreate , db : AsyncSession = Depends(get_db)):
    query = select(models.product).where(models.product.id == id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"محصولی با شناسه {id} برای ویرایش یافت نشد."
        )
        
    update_query = update(models.product).where(models.product.id == id).values(**new_data.model_dump())
    await db.execute(update_query)
    await db.commit

    updated_product_result = await db.execute(select(models.product).where(models.product.id == id))
    return updated_product_result.scalars().first()