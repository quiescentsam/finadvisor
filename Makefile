.PHONY: test backend rag multiagent shared coverage clean

test: backend rag multiagent shared

backend:
	cd backend && uv run pytest --cov=. --cov-report=term-missing

rag:
	cd rag && uv run pytest --cov=. --cov-report=term-missing

multiagent:
	cd multiagent && uv run pytest --cov=. --cov-report=term-missing

shared:
	cd shared && uv run pytest --cov=. --cov-report=term-missing

coverage:
	@echo "Generating combined coverage report..."
	rm -rf coverage
	mkdir coverage
	cd backend && cp -r htmlcov ../coverage/backend
	cd rag && cp -r htmlcov ../coverage/rag
	cd multiagent && cp -r htmlcov ../coverage/multiagent
	cd shared && cp -r htmlcov ../coverage/shared
	@echo "Combined coverage reports saved in ./coverage/"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
