from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Backend API"
    environment: str = "development"
    database_url: str | None = None
    jwt_secret_key: str | None = None
    log_level: str = "INFO"
    FINNHUB_API_KEY: str | None = None
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

    def require_database_url(self) -> str:
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        return self.database_url

    def require_jwt_secret_key(self) -> str:
        if not self.jwt_secret_key:
            raise RuntimeError("JWT_SECRET_KEY is not configured")
        return self.jwt_secret_key

    def require_finnhub_api_key(self) -> str:
        if not self.FINNHUB_API_KEY:
            raise RuntimeError("FINNHUB_API_KEY is not configured")
        return self.FINNHUB_API_KEY


settings = Settings()
