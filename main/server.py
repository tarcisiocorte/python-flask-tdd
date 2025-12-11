"""Flask server startup."""
from main.config.app import create_app

# Create Flask app instance
app = create_app()

if __name__ == '__main__':
    # Start the server
    app.run(debug=True, host='0.0.0.0', port=5000)

