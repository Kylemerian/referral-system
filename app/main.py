from fastapi import FastAPI
from app.routes import user, referral, referral_code

app = FastAPI()


app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(referral.router, prefix="/referral", tags=["referral"])
app.include_router(referral_code.router, prefix="/referral_code",
                   tags=["referral_code"])


@app.get("/")
async def root():
    return {"message": "Welcome to the referral system!"}
