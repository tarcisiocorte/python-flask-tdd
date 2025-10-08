#!/usr/bin/env python3
"""
Test runner script for Python Flask TDD project
Provides easy commands for running different types of tests
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the exit code"""
    if description:
        print(f"\n🔄 {description}")
        print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ {description} completed successfully")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return e.returncode


def main():
    parser = argparse.ArgumentParser(description="Python Flask TDD Test Runner")
    parser.add_argument("command", help="Test command to run")
    
    args = parser.parse_args()
    
    commands = {
        # Basic testing commands
        "test": {
            "cmd": ["python3", "-m", "pytest", "--tb=no", "-q"],
            "desc": "Running quick tests (quiet mode)"
        },
        "test:verbose": {
            "cmd": ["python3", "-m", "pytest", "-v"],
            "desc": "Running tests with verbose output"
        },
        "test:unit": {
            "cmd": ["python3", "-m", "pytest", "tests/", "-v", "--tb=short", "-m", "not integration and not slow"],
            "desc": "Running unit tests only"
        },
        "test:integration": {
            "cmd": ["python3", "-m", "pytest", "tests/integration/", "-v", "--tb=short"],
            "desc": "Running integration tests only"
        },
        "test:staged": {
            "cmd": ["python3", "-m", "pytest", "--lf", "-x"],
            "desc": "Running last failed tests"
        },
        "test:ci": {
            "cmd": ["python3", "-m", "pytest", "--cov=.", "--cov-report=html", "--cov-report=xml", "--cov-report=term-missing"],
            "desc": "Running CI tests with coverage"
        },
        "test:watch": {
            "cmd": ["python3", "-m", "pytest-watch", "--", "--tb=short"],
            "desc": "Running tests in watch mode"
        },
        "test:coverage": {
            "cmd": ["python3", "-m", "pytest", "--cov=.", "--cov-report=html", "--cov-report=term-missing"],
            "desc": "Running tests with coverage report"
        },
        
        # Code quality commands
        "lint": {
            "cmd": ["python3", "-m", "flake8", ".", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"],
            "desc": "Running linting (critical errors only)"
        },
        "lint:all": {
            "cmd": ["python3", "-m", "flake8", ".", "--count", "--statistics"],
            "desc": "Running full linting"
        },
        "format": {
            "cmd": ["python3", "-m", "black", "."],
            "desc": "Formatting code with black"
        },
        "format:check": {
            "cmd": ["python3", "-m", "black", "--check", "."],
            "desc": "Checking code formatting"
        },
        "type-check": {
            "cmd": ["python3", "-m", "mypy", "."],
            "desc": "Running type checking"
        },
        "security": {
            "cmd": ["python3", "-m", "bandit", "-r", ".", "-f", "json", "-o", "security-report.json"],
            "desc": "Running security scan"
        },
        
        # Development commands
        "start": {
            "cmd": ["python3", "app.py"],
            "desc": "Starting the Flask application"
        },
        "dev": {
            "cmd": ["python3", "-m", "flask", "run", "--debug", "--host=0.0.0.0", "--port=5000"],
            "desc": "Starting development server"
        },
        "debug": {
            "cmd": ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "app.py"],
            "desc": "Starting debug mode"
        },
        "install": {
            "cmd": ["pip", "install", "-r", "requirements.txt"],
            "desc": "Installing dependencies"
        },
        "install:dev": {
            "cmd": ["pip", "install", "-r", "requirements-dev.txt"],
            "desc": "Installing development dependencies"
        },
        "clean": {
            "cmd": ["python3", "-c", "import os, shutil; [os.remove(os.path.join(root, file)) for root, dirs, files in os.walk('.') for file in files if file.endswith('.pyc')]; [shutil.rmtree(os.path.join(root, dir)) for root, dirs, files in os.walk('.') for dir in dirs if dir == '__pycache__']"],
            "desc": "Cleaning Python cache files"
        }
    }
    
    if args.command not in commands:
        print(f"❌ Unknown command: {args.command}")
        print("\nAvailable commands:")
        for cmd in sorted(commands.keys()):
            print(f"  {cmd}")
        sys.exit(1)
    
    command_info = commands[args.command]
    exit_code = run_command(command_info["cmd"], command_info["desc"])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
