run-api:
	cd backend && uv run uvicorn app.main:app --reload

run-rag:
	cd rag && uv run python -m rag.pipeline
