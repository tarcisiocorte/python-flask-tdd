# Python Flask TDD Makefile
# Provides easy commands for testing and development

.PHONY: help test test-verbose test-unit test-integration test-staged test-ci test-watch test-coverage lint lint-all format format-check type-check security start dev debug install install-dev clean clean-all db-up db-down db-restart db-logs db-shell db-clean

PYTHON ?= $(shell if [ -x ./venv/bin/python3 ]; then echo ./venv/bin/python3; elif [ -x ./.venv/bin/python ]; then echo ./.venv/bin/python; else echo python3; fi)
MONGO_TEST_CONTAINER ?= flask-tdd-mongodb-test
MONGO_TEST_PORT ?= 27018
MONGO_TEST_USER ?= flask_user
MONGO_TEST_PASSWORD ?= test_password
MONGO_TEST_DB ?= flask_db

# Default target
help:
	@echo "Python Flask TDD - Available Commands:"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           - Run quick tests (quiet mode)"
	@echo "  test-verbose   - Run tests with verbose output"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-middleware - Run middleware tests only"
	@echo "  test-staged    - Run last failed tests"
	@echo "  test-ci        - Run CI tests with coverage"
	@echo "  test-watch     - Run tests in watch mode"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  lint           - Run linting (critical errors only)"
	@echo "  lint-all       - Run full linting"
	@echo "  format         - Format code with black"
	@echo "  format-check   - Check code formatting"
	@echo "  type-check     - Run type checking"
	@echo "  security       - Run security scan"
	@echo ""
	@echo "Development Commands:"
	@echo "  start          - Start the Flask application (new structure)"
	@echo "  start-legacy   - Start using legacy app.py"
	@echo "  dev            - Start development server"
	@echo "  debug          - Start debug mode"
	@echo "  install        - Install dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo "  clean          - Clean Python cache files"
	@echo "  clean-all      - Clean all generated files"
	@echo ""
	@echo "Database Commands:"
	@echo "  db-up          - Start PostgreSQL container"
	@echo "  db-down        - Stop PostgreSQL container"
	@echo "  db-restart     - Restart PostgreSQL container"
	@echo "  db-logs        - View PostgreSQL logs"
	@echo "  db-shell       - Access PostgreSQL shell"
	@echo "  db-clean       - Remove PostgreSQL container and volume (WARNING: deletes data)"
	@echo ""
	@echo "Usage: make <command>"
	@echo "Example: make test-unit"

# Testing commands
test:
	$(PYTHON) -m pytest --tb=no -q

test-verbose:
	$(PYTHON) -m pytest -v

test-unit:
	$(PYTHON) -m pytest tests/ -v --tb=short -m "not integration and not slow"

test-integration:
	@docker rm -f $(MONGO_TEST_CONTAINER) >/dev/null 2>&1 || true
	@docker run -d --name $(MONGO_TEST_CONTAINER) \
		-p $(MONGO_TEST_PORT):27017 \
		-e MONGO_INITDB_ROOT_USERNAME=$(MONGO_TEST_USER) \
		-e MONGO_INITDB_ROOT_PASSWORD=$(MONGO_TEST_PASSWORD) \
		-e MONGO_INITDB_DATABASE=$(MONGO_TEST_DB) \
		mongo:7-jammy >/dev/null
	@status=1; \
	for attempt in $$(seq 1 30); do \
		if docker exec $(MONGO_TEST_CONTAINER) mongosh \
			-u "$(MONGO_TEST_USER)" \
			-p "$(MONGO_TEST_PASSWORD)" \
			--authenticationDatabase admin \
			--quiet \
			--eval "db.adminCommand('ping').ok" >/dev/null 2>&1; then \
			status=0; \
			break; \
		fi; \
		sleep 1; \
	done; \
	if [ $$status -ne 0 ]; then \
		docker logs $(MONGO_TEST_CONTAINER); \
		docker rm -f $(MONGO_TEST_CONTAINER) >/dev/null; \
		exit $$status; \
	fi; \
	MONGO_URL="mongodb://$(MONGO_TEST_USER):$(MONGO_TEST_PASSWORD)@localhost:$(MONGO_TEST_PORT)/?authSource=admin" \
	MONGO_DB_NAME="$(MONGO_TEST_DB)" \
	$(PYTHON) -m pytest tests/ -v --tb=short -m "integration"; \
	status=$$?; \
	docker rm -f $(MONGO_TEST_CONTAINER) >/dev/null; \
	exit $$status

test-middleware:
	$(PYTHON) -m pytest tests/main/middlewares/ -v --tb=short

test-staged:
	$(PYTHON) -m pytest --lf -x

test-ci:
	$(PYTHON) -m pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing

test-watch:
	$(PYTHON) -m pytest-watch -- --tb=short

test-coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=html --cov-report=term-missing

# Code quality commands
lint:
	python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

lint-all:
	python -m flake8 . --count --statistics

format:
	python -m black .

format-check:
	python -m black --check .

type-check:
	python -m mypy .

security:
	python -m bandit -r . -f json -o security-report.json

# Development commands
start:
	python main/server.py

start-legacy:
	python app.py

dev:
	python -m flask run --debug --host=0.0.0.0 --port=5000

debug:
	python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main/server.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

clean-all: clean
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/ *.egg-info/ security-report.json

# Database commands
db-up:
	docker-compose up -d postgres
	@echo "PostgreSQL is starting. Check status with: make db-logs"

db-down:
	docker-compose stop postgres
	@echo "PostgreSQL container stopped. Data is preserved in volume."

db-restart:
	docker-compose restart postgres
	@echo "PostgreSQL container restarted."

db-logs:
	docker-compose logs -f postgres

db-shell:
	@POSTGRES_USER=$${POSTGRES_USER:-flask_user}; \
	POSTGRES_DB=$${POSTGRES_DB:-flask_db}; \
	docker-compose exec postgres psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"

db-clean:
	@echo "WARNING: This will delete the PostgreSQL container and all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "PostgreSQL container and volume removed."; \
	else \
		echo "Operation cancelled."; \
	fi
