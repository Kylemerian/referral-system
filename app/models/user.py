from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    referrals = relationship(
        "Referral", back_populates="referrer_user",
        foreign_keys="[Referral.referrer_id]")
    referral_code = relationship(
        "ReferralCode", uselist=False, back_populates="owner")
