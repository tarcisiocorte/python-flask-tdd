#!/bin/bash

# Integration test script - runs integration tests
echo "Running integration tests..."
python3 -m pytest tests/ -v --tb=short -m "integration"
