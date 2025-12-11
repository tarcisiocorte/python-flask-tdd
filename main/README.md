# Main Module - Flask Application Structure

This module contains the main Flask application structure, inspired by clean architecture principles and Express.js patterns.

## 📁 Structure

```
main/
├── config/
│   ├── __init__.py
│   ├── app.py           # Flask application factory
│   └── middlewares.py   # Middleware configuration
├── middlewares/
│   ├── __init__.py
│   └── body_parser.py   # Body parser middleware
├── server.py            # Server startup
└── README.md            # This file
```

## 🚀 Running the Application

### Method 1: Using the new structure (recommended)

```bash
python main/server.py
```

### Method 2: Using the legacy app.py

```bash
python app.py
```

Note: The legacy `app.py` now imports from the new structure for backwards compatibility.

## 📝 Files Overview

### `config/app.py`
Creates and configures the Flask application. This is the application factory that:
- Sets up middlewares
- Initializes dependencies (controllers, use cases, repositories)
- Defines routes
- Returns the configured Flask app instance

```python
from main.config.app import create_app

app = create_app()
```

### `config/middlewares.py`
Configures all middlewares for the Flask application. Currently includes:
- JSON Content-Type header setup
- `before_request` and `after_request` handlers
- Placeholder for future middleware (CORS, authentication, etc.)

### `middlewares/body_parser.py`
Contains middleware decorators for request body parsing:
- `body_parser`: Ensures request body is parsed (Flask handles this automatically)
- `json_content_type_required`: Validates Content-Type header for POST/PUT requests

### `server.py`
Entry point for starting the Flask server:
- Creates the app using the factory
- Starts the development server on port 5000

## 🧪 Testing

The middleware tests are located in `tests/main/middlewares/`:

```bash
# Run all main module tests
pytest tests/main/ -v

# Run only body parser tests
pytest tests/main/middlewares/test_body_parser.py -v
```

### Test Coverage

The `test_body_parser.py` includes:
- ✅ JSON body parsing test
- ✅ Signup route JSON parsing test
- ✅ Health check JSON response test

## 🔄 Comparison with Node.js/Express Structure

This structure mirrors the Node.js/Express pattern:

| Node.js/Express | Python/Flask |
|----------------|-------------|
| `src/main/config/app.ts` | `main/config/app.py` |
| `src/main/config/middlewares.ts` | `main/config/middlewares.py` |
| `src/main/middlewares/body-parser.ts` | `main/middlewares/body_parser.py` |
| `src/main/middlewares/body-parser.test.ts` | `tests/main/middlewares/test_body_parser.py` |
| `src/main/server.ts` | `main/server.py` |

## 🎯 Key Differences: Flask vs Express

### JSON Parsing
- **Express**: Requires explicit `body-parser` middleware
  ```javascript
  import { json } from 'express'
  export const bodyParser = json()
  ```

- **Flask**: Has built-in JSON support via `request.get_json()`
  ```python
  data = request.get_json()
  ```

### Middleware Pattern
- **Express**: Uses `app.use(middleware)`
- **Flask**: Uses decorators (`@app.before_request`, `@app.after_request`) or function wrappers

## 📚 Adding New Routes

Add routes in `main/config/app.py` inside the `create_app()` function:

```python
@app.route('/new-route', methods=['POST'])
def new_route():
    data = request.get_json()
    # Handle request
    return jsonify({'result': 'success'}), 200
```

## 🔧 Adding New Middlewares

1. Create middleware in `main/middlewares/`:
```python
# main/middlewares/my_middleware.py
from functools import wraps

def my_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Middleware logic
        return f(*args, **kwargs)
    return decorated_function
```

2. Configure in `main/config/middlewares.py`:
```python
from main.middlewares.my_middleware import my_middleware

def setup_middlewares(app: Flask) -> None:
    app.before_request(my_middleware)
```

3. Add tests in `tests/main/middlewares/test_my_middleware.py`

## 🌟 Benefits of This Structure

1. **Separation of Concerns**: Configuration, middleware, and server startup are separated
2. **Testability**: Each component can be tested independently
3. **Maintainability**: Easy to locate and modify specific functionality
4. **Scalability**: Simple to add new middlewares and routes
5. **Consistency**: Similar structure to Node.js/Express projects
6. **Clean Architecture**: Follows industry best practices

---

**Last Updated**: December 2025

