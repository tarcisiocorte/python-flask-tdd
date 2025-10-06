#!/bin/bash

# CI test script - runs all tests with coverage
echo "Running CI tests with coverage..."
python -m pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml
