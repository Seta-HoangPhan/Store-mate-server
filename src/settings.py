from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    default_password: str = "admin"
    auto_delete_expired_otp_time: int = 10  # in minutes

    class Config:
        env_file = ".env"


settings = Settings()
