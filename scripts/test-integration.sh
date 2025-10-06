#!/bin/bash

# Integration test script - runs integration tests
echo "Running integration tests..."
python -m pytest tests/integration/ -v --tb=short
