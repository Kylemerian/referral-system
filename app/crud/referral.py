from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.referral import Referral
from datetime import datetime, timezone


async def add_referral(db: AsyncSession, referrer_id: int, referred_id: int):
    db_referral = Referral(
        referrer_id=referrer_id,
        referred_id=referred_id,
        registered_at=datetime.now(timezone.utc)
    )
    db.add(db_referral)
    await db.commit()
    await db.refresh(db_referral)
    return db_referral


async def get_referrals_by_referrer(db: AsyncSession, referrer_id: int):
    result = await db.execute(select(Referral).
                              filter(Referral.referrer_id == referrer_id))
    return result.scalars().all()
