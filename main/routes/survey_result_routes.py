"""Survey result route registration."""

from flask import Flask

from main.adapters import adapt_route
from main.factories.controllers import (
    make_load_survey_result_controller,
    make_save_survey_result_controller,
)


def register_survey_result_routes(app: Flask) -> None:
    """Register routes used to save and load a survey result."""
    app.add_url_rule(
        "/api/surveys/<survey_id>/results",
        "api_save_survey_result",
        adapt_route(make_save_survey_result_controller()),
        methods=["PUT"],
    )
    app.add_url_rule(
        "/api/surveys/<survey_id>/results",
        "api_load_survey_result",
        adapt_route(make_load_survey_result_controller()),
        methods=["GET"],
    )
