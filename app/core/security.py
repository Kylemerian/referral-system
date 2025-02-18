from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from app.core.config import settings
import httpx


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HUNTER_API_URL = "https://api.hunter.io/v2/email-verifier"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict,
                        expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """Декодирование JWT-токена и проверка его валидности."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def validate_email(email: str) -> bool:
    """Проверка email через Hunter.io API"""
    params = {
        "email": email,
        "api_key": settings.API_KEY_HUNTER,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(HUNTER_API_URL, params=params)

    if response.status_code != 200:
        return False

    data = response.json()
    return data["data"]["status"] == "valid"
