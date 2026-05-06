from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.logging_utils import get_logger
from rag.pipeline import run_rag
from backend.config.settings import settings

from backend.app.routes import stocks
# from backend.app.routes import portfolio
# from backend.app.routes import users
from backend.app.routes import ai

logger = get_logger(__name__)

API_V1_PREFIX = "/api/v1"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Hello from FastAPI", "api_v1": API_V1_PREFIX}


v1_router = APIRouter(prefix=API_V1_PREFIX)


@v1_router.get("/rag")
def rag_endpoint(q: str):
    response = run_rag(q)
    logger.info("RAG endpoint hit")
    return {"response": response}


# Versioned API surface
v1_router.include_router(stocks.router)
# v1_router.include_router(portfolio.router)
# v1_router.include_router(users.router)
v1_router.include_router(ai.router)

app.include_router(v1_router)