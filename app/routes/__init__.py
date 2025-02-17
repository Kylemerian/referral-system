from fastapi import APIRouter
from app.routes.referral_code import router as referral_code_router
from app.routes.referral import router as referral_router

api_router = APIRouter()
api_router.include_router(referral_code_router,
                          prefix="/referral-code", tags=["Referral Codes"])
api_router.include_router(
    referral_router, prefix="/referrals", tags=["Referrals"])
