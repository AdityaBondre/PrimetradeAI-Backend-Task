from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Primetrade API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "primetrade_db")
    DATABASE_URL: str | None = None
    SQLITE_DB: str = "test.db"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if self.DATABASE_URL:
            # Render/Heroku often use postgres://, but SQLAlchemy/asyncpg needs postgresql+asyncpg://
            url = self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
            if "postgresql+asyncpg://" not in url:
                url = url.replace("postgresql://", "postgresql+asyncpg://")
            return url
        
        if os.getenv("USE_SQLITE", "true") == "true":
            return f"sqlite+aiosqlite:///./{self.SQLITE_DB}"
            
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-for-development")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
