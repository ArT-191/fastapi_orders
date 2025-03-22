from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://fastapi_user:password@localhost/fastapi_orders"
    REDIS_HOST: str = "localhost"  # Добавляем поддержку Redis
    REDIS_PORT: int = 6379  # Добавляем порт Redis

    class Config:
        env_file = ".env"

settings = Settings()
