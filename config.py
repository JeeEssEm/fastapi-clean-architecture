import os
import uuid
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 0
    DB_NAME: str = 'db'
    DB_USER: str = 'pguser'
    DB_PASSWORD: str = 'password'
    INIT_MODELS: bool = True
    HOST: str = '127.0.0.1'
    PORT: int = 8000

    VERIFIED: bool = True
    SECRET_KEY: str = '123'  # str(uuid.uuid4())
    REFRESH_TOKEN_EXPIRES: int = 30
    ACCESS_TOKEN_EXPIRES: int = 30


settings = Settings()


def get_database_url():
    return 'sqlite+aiosqlite:///./db.sqlite'
