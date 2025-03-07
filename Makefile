.PHONY: help install test lint format up down

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run app
	@flet run app.py

test: ## Run tests
	python -m unittest discover -s tests

lint: ## Run linter
	python -m ruff check .

format: ## Format code
	python -m black .

up: ## Start services
	docker-compose -f compose.yaml up -d

down: ## Stop services
	docker-compose -f compose.yaml down


.DEFAULT_GOAL := help