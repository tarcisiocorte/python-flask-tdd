"""Application route registration."""

from flask import Flask

from main.routes import (
    register_login_routes,
    register_survey_result_routes,
    register_survey_routes,
)


def setup_routes(app: Flask) -> None:
    """Register every public API route on the Flask application."""
    register_login_routes(app)
    register_survey_routes(app)
    register_survey_result_routes(app)
