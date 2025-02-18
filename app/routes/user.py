from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app import crud, schemas
from app.core.database import get_db
from app.core.security import validate_email
from app.core.security import create_access_token
from app.crud.user import get_user_by_email
from app.crud.user import verify_user_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    """Регистрация пользователя с валидацией email"""

    is_valid_email = await validate_email(user.email)
    if not is_valid_email:
        raise HTTPException(status_code=400, detail="Недействительный email")

    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email уже зарегистрирован")

    new_user = await crud.create_user(db, user)
    return new_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)
):
    user = await verify_user_password(db, form_data.email,
                                      form_data.password)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
