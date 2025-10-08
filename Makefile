# Python Flask TDD Makefile
# Provides easy commands for testing and development

.PHONY: help test test-verbose test-unit test-integration test-staged test-ci test-watch test-coverage lint lint-all format format-check type-check security start dev debug install install-dev clean clean-all

# Default target
help:
	@echo "Python Flask TDD - Available Commands:"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           - Run quick tests (quiet mode)"
	@echo "  test-verbose   - Run tests with verbose output"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
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
	@echo "  start          - Start the Flask application"
	@echo "  dev            - Start development server"
	@echo "  debug          - Start debug mode"
	@echo "  install        - Install dependencies"
	@echo "  install-dev    - Install development dependencies"
	@echo "  clean          - Clean Python cache files"
	@echo "  clean-all      - Clean all generated files"
	@echo ""
	@echo "Usage: make <command>"
	@echo "Example: make test-unit"

# Testing commands
test:
	python -m pytest --tb=no -q

test-verbose:
	python -m pytest -v

test-unit:
	python -m pytest tests/ -v --tb=short -m "not integration and not slow"

test-integration:
	python -m pytest tests/integration/ -v --tb=short

test-staged:
	python -m pytest --lf -x

test-ci:
	python -m pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing

test-watch:
	python -m pytest-watch -- --tb=short

test-coverage:
	python -m pytest --cov=. --cov-report=html --cov-report=term-missing

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
	python app.py

dev:
	python -m flask run --debug --host=0.0.0.0 --port=5000

debug:
	python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

clean-all: clean
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/ *.egg-info/ security-report.json
