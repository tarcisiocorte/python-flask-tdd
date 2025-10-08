#!/bin/bash

# Unit test script - runs only unit tests
echo "Running unit tests..."
python -m pytest tests/ -v --tb=short -m "not integration and not slow"
