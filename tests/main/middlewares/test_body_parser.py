"""Tests for body parser middleware."""
import unittest
import json
from main.config.app import create_app


class TestBodyParserMiddleware(unittest.TestCase):
    """Test suite for body parser middleware."""
    
    def setUp(self):
        """Set up test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_should_parse_body_as_json(self):
        """Test that the application correctly parses JSON request body."""
        # Create a test route
        @self.app.route('/test_body_parser', methods=['POST'])
        def test_route():
            from flask import request, jsonify
            return jsonify(request.get_json())
        
        # Make request with JSON body
        response = self.client.post(
            '/test_body_parser',
            data=json.dumps({'name': 'Rodrigo'}),
            content_type='application/json'
        )
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {'name': 'Rodrigo'})
    
    def test_signup_route_parses_json_body(self):
        """Test that the signup route correctly parses JSON body."""
        # Test with valid signup data
        signup_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'passwordConfirmation': 'password123'
        }
        
        response = self.client.post(
            '/signup',
            data=json.dumps(signup_data),
            content_type='application/json'
        )
        
        # Assert response is valid JSON
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        
        # Assert response structure
        self.assertIn('success', data)
        
    def test_health_check_returns_json(self):
        """Test that health check endpoint returns JSON."""
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data, {'status': 'healthy'})


if __name__ == '__main__':
    unittest.main()

