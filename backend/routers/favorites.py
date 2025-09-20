from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Favorite, Product, User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class FavoriteResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    product_image: Optional[str]

    class Config:
        from_attributes = True

@router.post("/{product_id}")
async def add_favorite(product_id: int, telegram_id: str, db: AsyncSession = Depends(get_db)):
    # Get user
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if product exists
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if already favorite
    result = await db.execute(select(Favorite).where(Favorite.user_id == user.id, Favorite.product_id == product_id))
    favorite = result.scalar_one_or_none()
    if favorite:
        raise HTTPException(status_code=400, detail="Already in favorites")
    
    favorite = Favorite(user_id=user.id, product_id=product_id)
    db.add(favorite)
    await db.commit()
    return {"message": "Added to favorites"}

@router.delete("/{product_id}")
async def remove_favorite(product_id: int, telegram_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(select(Favorite).where(Favorite.user_id == user.id, Favorite.product_id == product_id))
    favorite = result.scalar_one_or_none()
    if not favorite:
        raise HTTPException(status_code=404, detail="Not in favorites")
    
    await db.delete(favorite)
    await db.commit()
    return {"message": "Removed from favorites"}

@router.get("/", response_model=List[FavoriteResponse])
async def get_favorites(telegram_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = select(Favorite, Product).join(Product).where(Favorite.user_id == user.id)
    result = await db.execute(query)
    items = result.all()
    return [
        FavoriteResponse(
            id=fav.id,
            product_id=prod.id,
            product_name=prod.name,
            product_price=prod.price,
            product_image=prod.image_url
        ) for fav, prod in items
    ]