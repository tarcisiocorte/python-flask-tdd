"""Setup middlewares for Flask application."""
from flask import Flask


def setup_middlewares(app: Flask) -> None:
    """
    Configure all middlewares for the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Flask automatically handles JSON parsing when Content-Type is application/json
    # Additional middleware configuration can be added here
    
    # Example: CORS middleware (if needed in the future)
    # from flask_cors import CORS
    # CORS(app)
    
    # Example: Custom before_request handlers
    @app.before_request
    def before_request():
        """Execute before each request."""
        pass
    
    # Example: Custom after_request handlers
    @app.after_request
    def after_request(response):
        """Execute after each request."""
        # Ensure JSON responses have correct Content-Type
        if response.get_json() is not None:
            response.headers['Content-Type'] = 'application/json'
        return response

