from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    referrer_user = relationship(
        "User", foreign_keys=[referrer_id], back_populates="referrals")
    referred_user = relationship("User", foreign_keys=[referred_id])
