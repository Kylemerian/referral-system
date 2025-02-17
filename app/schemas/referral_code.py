from pydantic import BaseModel
from datetime import datetime


class ReferralCodeBase(BaseModel):
    code: str


class ReferralCodeCreate(ReferralCodeBase):
    expires_at: datetime


class ReferralCodeResponse(ReferralCodeBase):
    id: int
    owner_id: int
    expires_at: datetime

    class Config:
        from_attributes = True
