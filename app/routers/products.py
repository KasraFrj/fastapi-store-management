from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/products" , tags=["Products"])

@router.post("/create" , response_model=schemas.ProductOut)
def create_product(product_data : schemas.ProductCreate , db : Session = Depends(get_db)):
    new_product = models.product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/read_product" , response_model=List[schemas.ProductOut])
def read_product(db : Session = Depends(get_db)):
    products = db.query(models.product).all()
    return products

@router.get("/read_product/{id}" , response_model=schemas.ProductOut)
def get_one_product(id : str , db : Session = Depends(get_db)):
    db_product = db.query(models.product).filter(models.product.id == id).first()
    if not db_product:
        raise HTTPException(status_code = 404 , detail=f" {id} Not Found")
    return db_product

@router.delete("/delete/{id}")
def delete_product(id : int , db : Session = Depends(get_db)):
    product_query = db.query(models.product).filter(models.product.id == id)
    product = product_query.first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"محصولی با شناسه {id} برای حذف یافت نشد."
        )
        
    product_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "محصول با موفقیت حذف شد."}

@router.put("/update/{id}" , response_model=schemas.ProductOut)
def update_product(id : int , new_data : schemas.ProductCreate , db : Session = Depends(get_db)):
    product_query = db.query(models.product).filter(models.product.id == id)
    product = product_query.first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"محصولی با شناسه {id} برای ویرایش یافت نشد."
        )
        
    product_query.update(new_data.model_dump(), synchronize_session=False)
    db.commit()
    return product_query.first()