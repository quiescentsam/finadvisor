run-api:
	cd backend && uv run uvicorn backend.app.main:app --reload

run-rag:
	cd rag && uv run python -m rag.pipeline

run-ui:
	cd frontend && uv run streamlit run frontend/streamlit_app.py
