from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.referral_code import ReferralCode
from app.models.user import User
from datetime import datetime, timezone


async def create_referral_code(db: AsyncSession, owner_id: int,
                               code: str, expires_at: datetime):
    db_code = ReferralCode(code=code, owner_id=owner_id,
                           expires_at=expires_at.replace(tzinfo=timezone.utc))
    db.add(db_code)
    await db.commit()
    await db.refresh(db_code)
    return db_code


async def get_referral_code_by_user(db: AsyncSession, owner_id: int):
    result = await db.execute(select(ReferralCode).
                              filter(ReferralCode.owner_id == owner_id))
    return result.scalars().first()


async def get_referral_code_by_email(db: AsyncSession, owner_email: str):
    result = await db.execute(
        select(ReferralCode)
        .join(User, User.id == ReferralCode.owner_id)
        .filter(User.email == owner_email)
    )
    return result.scalars().first()


async def delete_referral_code(db: AsyncSession, owner_id: int):
    result = await db.execute(select(ReferralCode).
                              filter(ReferralCode.owner_id == owner_id))
    code = result.scalars().first()
    if code:
        await db.delete(code)
        await db.commit()
        return True
    return False
