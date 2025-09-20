from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Product
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    old_price: Optional[float]
    discount: Optional[float]
    image_url: Optional[str]
    product_url: str
    partner_url: str
    rating: Optional[float]
    category: str
    shop: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category: Optional[str] = Query(None),
    shop: Optional[str] = Query(None),
    min_discount: Optional[float] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Product)
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))
    if shop:
        query = query.where(Product.shop.ilike(f"%{shop}%"))
    if min_discount:
        query = query.where(Product.discount >= min_discount)
    
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return [ProductResponse.from_orm(p) for p in products]

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_orm(product)

# TODO: Add search endpoint with keywords