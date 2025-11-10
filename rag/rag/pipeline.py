from shared.logging_utils import get_logger

logger = get_logger(__name__)

def run_rag(query: str):
    logger.info(f"Running RAG for query: {query}")
    # placeholder
    return f"Answer to '{query}' from RAG"