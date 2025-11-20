from sqlalchemy import create_engine
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_engine(settings.database_url)
