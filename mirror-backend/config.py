from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    sentry_dsn: str

    class Config:
        env_file = ".env"

settings = Settings()
