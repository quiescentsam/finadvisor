from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Backend API"
    environment: str = "development"
    database_url: str
    jwt_secret_key: str
    log_level: str = "INFO"
    FINNHUB_API_KEY: str
    # Comma-separated origins for CORS (include your Render frontend URL in production).
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

settings = Settings()
