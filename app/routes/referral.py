from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.referral import ReferralCreate, ReferralResponse
from app.crud.referral import add_referral, get_referrals_by_referrer
from app.crud.referral_code import get_referral_code_by_user
from app.core.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=ReferralResponse)
async def register_by_referral(referrer_id: int, referred_id: int,
                               db: AsyncSession = Depends(get_db)):
    """Регистрация нового пользователя по реферальному коду."""
    referral_code = await get_referral_code_by_user(db, referrer_id)
    if not referral_code:
        raise HTTPException(
            status_code=404, detail="Реферальный код не найден")

    return await add_referral(db, referrer_id, referred_id)


@router.get("/{referrer_id}", response_model=List[ReferralResponse])
async def get_referrals(referrer_id: int, db: AsyncSession = Depends(get_db)):
    """Получение списка рефералов по ID реферера."""
    return await get_referrals_by_referrer(db, referrer_id)
