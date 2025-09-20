from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from auth import get_user_from_init_data
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_premium: bool

    class Config:
        from_attributes = True

@router.post("/auth", response_model=UserResponse)
async def authenticate_user(init_data: str, db: AsyncSession = Depends(get_db)):
    try:
        user_data = get_user_from_init_data(init_data)
        telegram_id = str(user_data['id'])
        
        # Check if user exists
        result = await db.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=user_data.get('username'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name')
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        return UserResponse.from_orm(user)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)