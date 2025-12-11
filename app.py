"""
LEGACY FILE - This file is kept for backwards compatibility.

The application has been refactored to follow a better structure:
- main/config/app.py - Application factory and configuration
- main/config/middlewares.py - Middleware setup
- main/middlewares/ - Individual middleware implementations
- main/server.py - Server startup

To use the new structure, run:
    python main/server.py

Or import from:
    from main.config.app import create_app
"""
from main.config.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
