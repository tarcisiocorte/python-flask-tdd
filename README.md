# Python Flask TDD Project

A Python Flask application built using Test-Driven Development (TDD) principles with a clean architecture approach. This project demonstrates a signup functionality with proper separation of concerns and comprehensive unit testing.

## 🏗️ Project Structure

```
python-flask-tdd/
├── domain/                    # Domain layer (business logic)
│   ├── models/               # Domain entities
│   │   └── account.py        # Account model
│   └── usecases/             # Business use cases
│       └── add_account.py    # Add account use case
├── errors/                   # Custom error classes
│   ├── missing_param_error.py
│   └── server_error.py
├── presentation/             # Presentation layer
│   ├── helpers/              # Helper functions
│   └── signup.py             # Signup presentation logic
├── protocols/                # Interface definitions
│   ├── http.py               # HTTP request/response models
│   └── signup_protocols.py   # Signup-related protocols
├── signup.py                 # Main signup controller
├── test_signup_controller.py # Unit tests for signup controller
├── requirements.txt          # Python dependencies
└── README.md                 # This file
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

This project uses `pytest` for unit testing. Here are the different ways to run the tests:

### Run All Tests
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Coverage Report
```bash
pytest --cov=.
```

### Run Specific Test File
```bash
pytest test_signup_controller.py
```

### Run Tests with Detailed Output
```bash
pytest -v -s
```

### Run Tests Using Python's Built-in unittest
```bash
python -m unittest test_signup_controller.py
```

### Run Tests and Generate HTML Coverage Report
```bash
pytest --cov=. --cov-report=html
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