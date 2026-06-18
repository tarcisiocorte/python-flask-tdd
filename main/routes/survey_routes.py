"""Survey route registration."""

from flask import Flask

from main.adapters import adapt_route
from main.factories.controllers import (
    make_add_survey_controller,
    make_load_surveys_controller,
)


def register_survey_routes(app: Flask) -> None:
    """Register survey creation and listing routes."""
    app.add_url_rule(
        "/api/surveys",
        "api_add_survey",
        adapt_route(make_add_survey_controller()),
        methods=["POST"],
    )
    app.add_url_rule(
        "/api/surveys",
        "api_load_surveys",
        adapt_route(make_load_surveys_controller()),
        methods=["GET"],
    )
