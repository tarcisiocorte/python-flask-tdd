"""Flask application factory and configuration."""

from flask import Flask, jsonify

from main.config.middlewares import setup_middlewares
from main.config.routes import setup_routes


def create_app() -> Flask:
    app = Flask(__name__)
    setup_middlewares(app)
    setup_routes(app)

    @app.route("/health", methods=["GET"])
    def health() -> tuple:
        return jsonify({"status": "healthy"}), 200

    return app
