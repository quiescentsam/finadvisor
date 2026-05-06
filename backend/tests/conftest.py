import os

# Settings() loads at import time; tests must not require a real .env.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-for-pytest")
os.environ.setdefault("FINNHUB_API_KEY", "test-finnhub-key")
