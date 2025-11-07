from fastapi import FastAPI
from shared.utils.logger import get_logger

app = FastAPI(title="GenAI Backend API")
logger = get_logger(__name__)

@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "GenAI Backend is running!"}
