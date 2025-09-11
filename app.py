from flask import Flask, request, jsonify
from presentation.controllers.signup_controller import SignUpController
from presentation.helpers.email_validator_adapter import EmailValidatorAdapter
from infrastructure.add_account_repository import AddAccountRepository
from protocols.http import HttpRequest
import json


def create_app():
    app = Flask(__name__)
    
    # Initialize dependencies
    email_validator = EmailValidatorAdapter()
    add_account_repository = AddAccountRepository()
    signup_controller = SignUpController(email_validator, add_account_repository)
    
    @app.route('/signup', methods=['POST'])
    def signup():
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
        return jsonify({'status': 'healthy'}), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
