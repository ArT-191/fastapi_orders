import redis
from app.config import settings  # Убедись, что у тебя есть конфиг с настройками

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)
