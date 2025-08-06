from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    database_url: str

    default_password: str
    auto_delete_expired_otp_time: int = 10  # in minutes

    access_token_key: str
    refresh_token_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30  # in minutes
    refresh_token_expire_hours: int = 20  # in hours

    cloud_name: str
    api_key: str
    api_secret: str

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")


settings = Settings()
