run-api:
	cd backend && uv run uvicorn backend.app.main:app --reload

run-rag:
	cd rag && uv run python -m rag.pipeline

install-ui:
	cd frontend && npm install

run-ui:
	cd frontend && npm run dev
