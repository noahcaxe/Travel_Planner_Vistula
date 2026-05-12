from pydantic_settings import BaseSettings
import os 
from pathlib import Path






class Settings(BaseSettings):
    APP_NAME : str
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    JWT_SECRET: str
    JWT_ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



settings = Settings()
