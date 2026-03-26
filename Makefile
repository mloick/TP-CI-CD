.PHONY: install start test lint format

install:
	pip install -r requirements.txt

start:
	python app.py

test:
	pytest

lint:
	flake8 .

format:
	black .
