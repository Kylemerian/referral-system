import redis.asyncio as redis
from app.core.config import settings


async def get_redis():
    client = redis.Redis(host=settings.REDIS_URL,
                         port=6379, db=0, decode_responses=True)
    return client
