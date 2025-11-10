from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Backend API"
    environment: str = "development"
    database_url: str
    jwt_secret_key: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
