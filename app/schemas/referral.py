from pydantic import BaseModel
from datetime import datetime


class ReferralBase(BaseModel):
    referrer_id: int
    referred_id: int


class ReferralCreate(ReferralBase):
    pass


class ReferralResponse(ReferralBase):
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True
