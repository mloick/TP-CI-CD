.PHONY: install start test lint format

install:
	pip install -r requirements.txt

start:
	PYTHONPATH=. python src/app.py

test:
	PYTHONPATH=. pytest --cov=src tests/

lint:
	flake8 src/ tests/

format:
	black src/ tests/
