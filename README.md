# Python Flask TDD Project

A Python Flask application built using Test-Driven Development (TDD) principles with a clean architecture approach. This project demonstrates a signup functionality with proper separation of concerns and comprehensive unit testing.

## 🏗️ Project Structure

```
python-flask-tdd/
├── data/                      # Data layer (infrastructure)
│   ├── protocols/            # Data layer protocols
│   │   ├── encrypter.py      # Encryption protocol
│   │   └── add_account_repository.py  # Repository protocol
│   └── usecases/             # Data usecases implementations
│       └── add_account/      # Add account usecase
│           ├── db_add_account.py
│           ├── db_add_account_protocols.py
│           └── in_memory_add_account_repository.py
├── domain/                    # Domain layer (business logic)
│   ├── models/               # Domain entities
│   │   └── account.py        # Account model
│   └── usecases/             # Business use cases
│       └── add_account.py    # Add account use case interface
├── presentation/             # Presentation layer
│   ├── controllers/          # Controllers
│   │   └── signup/           # Signup controller
│   │       ├── signup.py
│   │       └── signup_protocols.py
│   ├── errors/               # Presentation errors
│   │   ├── invalid_param_error.py
│   │   ├── missing_param_error.py
│   │   └── server_error.py
│   ├── helpers/              # Helper functions
│   │   └── http_helper.py
│   └── protocols/            # Presentation protocols
│       ├── controller.py
│       ├── email_validator.py
│       └── http.py
├── utils/                     # Utility adapters
│   ├── email_validator_adapter.py
│   └── bcrypt_encrypter.py
├── tests/                     # Test files
│   ├── data/
│   ├── presentation/
│   └── utils/
├── app.py                     # Flask application
├── conftest.py                # Pytest configuration
├── test_runner.py              # Test runner script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Features

- **Clean Architecture**: Separation of concerns with domain, use cases, and presentation layers
- **TDD Approach**: Test-driven development with comprehensive unit tests
- **Error Handling**: Proper error handling with custom error classes
- **Input Validation**: Request validation for signup parameters
- **Password Confirmation**: Password matching validation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository** (if using version control):
   ```bash
   git clone <repository-url>
   cd python-flask-tdd
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Running Unit Tests

This project uses `pytest` for unit testing. You can run tests in multiple ways:

### 🚀 Quick Commands (Recommended)

#### Using the Test Runner Script

**First, make sure your virtual environment is activated:**
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

Then run the tests:
```bash
# Unit tests only (recommended for unit testing)
python test_runner.py test:unit

# Quick test run (quiet mode)
python test_runner.py test

# Verbose test output
python test_runner.py test:verbose

# Tests with coverage report
python test_runner.py test:coverage

# CI tests with coverage (includes XML report)
python test_runner.py test:ci

# Run last failed tests
python test_runner.py test:staged

# Watch mode for development (auto-reruns on file changes)
python test_runner.py test:watch

# Integration tests only
python test_runner.py test:integration
```

**Note:** The test runner script requires the virtual environment to be activated to access pytest and other dependencies.

#### Using Make Commands

**Make sure your virtual environment is activated first!**
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

Then run:
```bash
# Quick test run
make test

# Verbose test output
make test-verbose

# Unit tests only (recommended for unit testing)
make test-unit

# Integration tests only
make test-integration

# CI tests with coverage
make test-ci

# Watch mode for development
make test-watch

# Tests with coverage report
make test-coverage
```

### 🔧 Direct Python Commands

**Make sure your virtual environment is activated first!**

#### Run All Tests
```bash
pytest tests/ -v
```

#### Run Tests with Verbose Output
```bash
pytest tests/ -v
```

#### Run Unit Tests Only
```bash
pytest tests/ -v --tb=short
```

#### Run Tests with Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
```

#### Run Specific Test File
```bash
# Signup controller tests
pytest tests/presentation/controllers/signup/test_signup.py -v

# DbAddAccount tests
pytest tests/data/usecases/add_account/test_db_add_account.py -v

# Email validator tests
pytest tests/utils/test_email_validator_adapter.py -v
```

#### Run Tests in Watch Mode
```bash
pytest-watch -- --tb=short
```

### 📊 Code Quality Commands

#### Linting
```bash
# Critical errors only
python test_runner.py lint
# or
make lint

# Full linting
python test_runner.py lint:all
# or
make lint-all
```

#### Code Formatting
```bash
# Format code
python test_runner.py format
# or
make format

# Check formatting
python test_runner.py format:check
# or
make format-check
```

#### Type Checking
```bash
python test_runner.py type-check
# or
make type-check
```

#### Security Scan
```bash
python test_runner.py security
# or
make security
```

## 📝 Test Structure

The project includes comprehensive unit tests for the `SignUpController` class:

- **Input Validation Tests**: Verify that all required fields are provided
- **Password Confirmation Tests**: Ensure password and confirmation match
- **Success Case Tests**: Verify successful account creation
- **Error Handling Tests**: Test proper error responses for various scenarios
- **Integration Tests**: Verify correct interaction with dependencies

### Test Cases Covered

1. Missing required fields (name, email, password, passwordConfirmation)
2. Password confirmation mismatch
3. Successful signup with valid data
4. Server error handling
5. Correct parameter passing to dependencies

## 🏃‍♂️ Running the Application

Currently, this project focuses on the business logic and testing. To run a Flask web server, you would need to add a Flask application file. Here's a basic example of how you might set it up:

```python
from flask import Flask, request, jsonify
from signup import SignUpController
from domain.usecases.add_account import AddAccount

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    # Implementation would go here
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

## 🔧 Development

### Adding New Features

1. Write tests first (TDD approach)
2. Implement the feature
3. Ensure all tests pass
4. Refactor if necessary

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for public methods
- Keep functions small and focused

## 📦 Dependencies

The main dependencies include:

- **Flask**: Web framework
- **pytest**: Testing framework
- **unittest**: Python's built-in testing framework (used in tests)

See `requirements.txt` for the complete list of dependencies with specific versions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Implement the feature
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Include steps to reproduce the problem

---

**Happy coding! 🎉** 