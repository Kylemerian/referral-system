from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.referral_code import ReferralCodeCreate, ReferralCodeResponse
from app.crud.referral_code import create_referral_code
from app.crud.referral_code import get_referral_code_by_user
from app.crud.referral_code import delete_referral_code
from app.core.database import get_db
from datetime import datetime, timedelta, timezone
from typing import Optional

router = APIRouter()


@router.post("/", response_model=ReferralCodeResponse)
async def create_code(
    owner_id: int,
    expires_in_minutes: Optional[int] = 1440,
    db: AsyncSession = Depends(get_db),
):
    """Создание реферального кода с указанным сроком действия."""
    expires_at = datetime.now(timezone.utc) + \
        timedelta(minutes=expires_in_minutes)

    existing_code = await get_referral_code_by_user(db, owner_id)
    if existing_code:
        raise HTTPException(
            status_code=400, detail="У вас уже есть активный код")

    return await create_referral_code(db, owner_id, "random_code", expires_at)


@router.get("/{owner_id}", response_model=ReferralCodeResponse)
async def get_code(owner_id: int, db: AsyncSession = Depends(get_db)):
    """Получение реферального кода по ID владельца."""
    code = await get_referral_code_by_user(db, owner_id)
    if not code:
        raise HTTPException(status_code=404, detail="Код не найден")
    return code


@router.delete("/{owner_id}")
async def delete_code(owner_id: int, db: AsyncSession = Depends(get_db)):
    """Удаление реферального кода пользователя."""
    success = await delete_referral_code(db, owner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Код не найден")
    return {"message": "Реферальный код удален"}
