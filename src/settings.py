from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    org_email: str

    class Config:
        env_file = ".env"


settings = Settings()
