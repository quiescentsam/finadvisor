backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entrypoint (uvicorn runs this)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Environment-based config
│   │   └── logging_config.py    # Logging setup
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependencies (e.g., DB session)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes_users.py
│   │   │   ├── routes_auth.py
│   │   │   └── routes_health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py          # Auth, JWT, password hashing
│   │   ├── exceptions.py
│   │   └── utils.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── base.py              # Base SQLAlchemy model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py       # Pydantic models
│   │   └── auth_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── email_service.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py           # DB engine + session maker
│   │   └── init_db.py           # Initial data load / migrations
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py          # pytest fixtures
│       ├── test_users.py
│       └── test_auth.py
│
├── pyproject.toml               # Managed by uv
├── README.md
├── Makefile                     # Common dev commands
└── .env.example                 # Example environment file





Cd backend 

 uv run uvicorn backend.app.main:app --reload