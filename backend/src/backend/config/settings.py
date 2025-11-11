from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Backend API"
    environment: str = "development"
    database_url: str
    jwt_secret_key: str
    log_level: str = "INFO"
    FINNHUB_API_KEY: str

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
