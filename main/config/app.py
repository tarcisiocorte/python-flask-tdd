"""Flask application factory and configuration."""
from flask import Flask, request, jsonify
from main.config.middlewares import setup_middlewares
from presentation.controllers.signup.signup import SignUpController
from utils.email_validator_adapter import EmailValidatorAdapter
from data.usecases.add_account.db_add_account import DbAddAccount
from data.usecases.add_account.in_memory_add_account_repository import InMemoryAddAccountRepository
from utils.bcrypt_encrypter import BcryptEncrypter
from presentation.protocols.http import HttpRequest


def create_app() -> Flask:
    """
    Create and configure Flask application.
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Setup middlewares
    setup_middlewares(app)
    
    # Initialize dependencies
    email_validator = EmailValidatorAdapter()
    encrypter = BcryptEncrypter()
    add_account_repository = InMemoryAddAccountRepository()
    add_account = DbAddAccount(encrypter, add_account_repository)
    signup_controller = SignUpController(email_validator, add_account)
    
    # Routes
    @app.route('/signup', methods=['POST'])
    def signup():
        """Handle user signup requests."""
        try:
            # Get JSON data from request
            data = request.get_json()
            
            # Create HTTP request object
            http_request = HttpRequest(body=data)
            
            # Handle the request through the controller
            response = signup_controller.handle(http_request)
            
            # Convert response to Flask response
            if response.status_code == 200:
                return jsonify({
                    'success': True,
                    'data': {
                        'id': response.body.id,
                        'name': response.body.name,
                        'email': response.body.email
                    }
                }), response.status_code
            else:
                return jsonify({
                    'success': False,
                    'error': str(response.body)
                }), response.status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200
    
    return app

