.PHONY: run lint test 

PROJECT_PATH="src"

run:
	poetry run python $(PROJECT_PATH)/main.py

lint:
	@echo "==> Running isort....."
	poetry run isort $(PROJECT_PATH)
	@echo "==> Running black....."
	poetry run black $(PROJECT_PATH)
	@echo "==> Running mypy....."
	poetry run mypy $(PROJECT_PATH)
	@echo "==> Running vulture....."
	poetry run vulture $(PROJECT_PATH)
	@echo "==> Running bandit....."
	poetry run bandit -r $(PROJECT_PATH)

test:
	poetry run pytest -s -vv