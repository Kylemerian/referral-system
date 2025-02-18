from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.referral_code import ReferralCodeResponse
from app.crud.referral_code import create_referral_code
from app.crud.referral_code import get_referral_code_by_user
from app.crud.referral_code import get_referral_code_by_email
from app.crud.referral_code import delete_referral_code
from app.core.database import get_db
from app.core.security import decode_access_token
from app.crud.user import get_user_by_email
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.core.redis import get_redis
import secrets

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=ReferralCodeResponse)
async def create_code(
    owner_id: int,
    expires_in_minutes: Optional[int] = 1440,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    redis=Depends(get_redis),
):
    """Создание реферального кода с указанным сроком действия."""
    payload = decode_access_token(token)
    user_email = payload.get("sub")

    user = await get_user_by_email(db, user_email)
    if not user or user.id != owner_id:
        raise HTTPException(
            status_code=403,
            detail="Вы можете создавать только свой реферальный код")

    expires_at = datetime.now(timezone.utc) + \
        timedelta(minutes=expires_in_minutes)

    cached_code = await redis.get(f"referral_code:{owner_id}")
    if cached_code:
        raise HTTPException(
            status_code=400, detail="У вас уже есть активный код")

    existing_code = await get_referral_code_by_user(db, owner_id)
    if existing_code:
        raise HTTPException(
            status_code=400, detail="У вас уже есть активный код")

    random_code = secrets.token_urlsafe(12)
    await redis.setex(f"referral_code:{owner_id}", expires_in_minutes * 60,
                      random_code)
    return await create_referral_code(db, owner_id, random_code, expires_at)


# @router.get("/{owner_id}", response_model=ReferralCodeResponse)
# async def get_code(owner_id: int, db: AsyncSession = Depends(get_db)):
#     """Получение реферального кода по ID владельца."""
#     code = await get_referral_code_by_user(db, owner_id)
#     if not code:
#         raise HTTPException(status_code=404, detail="Код не найден")
#     return code


@router.get("/{owner_email}", response_model=ReferralCodeResponse)
async def get_code_by_email(
    owner_email: str,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    """Получение реферального кода по email владельца."""
    cached_code = await redis.get(f"referral_code:{owner_email}")
    if cached_code:
        return {"owner_email": owner_email, "code": cached_code}

    code = await get_referral_code_by_email(db, owner_email)
    if not code:
        raise HTTPException(status_code=404, detail="Код не найден")

    await redis.setex(f"referral_code:{owner_email}", 1440 * 60, code.code)

    return code


@router.delete("/{owner_id}")
async def delete_code(
    owner_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    redis=Depends(get_redis)
):
    """Удаление реферального кода, только если пользователь удаляет свой"""
    user_data = decode_access_token(token)
    user_id = user_data.get("sub")

    if not user_id or int(user_id) != owner_id:
        raise HTTPException(
            status_code=403, detail="Вы можете удалить только свой код"
        )

    success = await delete_referral_code(db, owner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Код не найден")

    await redis.delete(f"referral_code:{owner_id}")

    return {"message": "Реферальный код удален"}
