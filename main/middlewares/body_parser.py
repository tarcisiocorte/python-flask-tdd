"""Body parser middleware for Flask application."""
from flask import request, jsonify
from functools import wraps


def body_parser(f):
    """
    Middleware to ensure request body is parsed as JSON.
    This is more for consistency with Express.js pattern.
    Flask already handles JSON parsing automatically.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Flask automatically parses JSON if Content-Type is application/json
        # This middleware is a placeholder for future body parsing logic
        return f(*args, **kwargs)
    return decorated_function


def json_content_type_required(f):
    """
    Middleware to ensure Content-Type is application/json for POST/PUT requests.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                return jsonify({
                    'success': False,
                    'error': 'Content-Type must be application/json'
                }), 415
        return f(*args, **kwargs)
    return decorated_function

