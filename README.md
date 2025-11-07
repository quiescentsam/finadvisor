



uv add fastapi 'uvicorn[standard]' 'pydantic[dotenv]' httpx



## Run all tests 


Goal	Command
Run backend tests	cd backend && uv run pytest
Run rag tests	cd rag && uv run pytest
Run multiagent tests	cd multiagent && uv run pytest
Run shared tests	cd shared && uv run pytest
Run all tests	make test

make test


## COverage 
This ensures pytest always measures coverage of the current module.

uv add --dev pytest pytest-cov

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "--cov=."


uv run pytest --cov=. --cov-report=term-missing

## make file 

make test
make coverage