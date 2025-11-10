from fastapi import FastAPI
from shared.logging_utils import get_logger
from rag.pipeline import run_rag
from backend.config.settings import settings

logger = get_logger(__name__)
app = FastAPI()

@app.get("/")
def root():
    logger.info("Root endpoint hit")    
    print(settings.database_url)
    return {"message": "Hello from FastAPI"}

@app.get("/rag")
def rag_endpoint(q: str):
    response = run_rag(q)
    logger.info("RAG endpoint hit")
    return {"response": response}
