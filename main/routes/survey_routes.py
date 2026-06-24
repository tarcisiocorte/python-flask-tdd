"""Survey route registration."""

from flask import Flask

from main.adapters import adapt_middleware, adapt_route
from main.factories.controllers import (
    make_add_survey_controller,
    make_load_surveys_controller,
)
from main.factories.middlewares import make_auth_middleware


def register_survey_routes(app: Flask) -> None:
    """Register survey creation and listing routes."""
    admin_auth = adapt_middleware(make_auth_middleware("admin"))
    auth = adapt_middleware(make_auth_middleware())

    app.add_url_rule(
        "/api/surveys",
        "api_add_survey",
        admin_auth(adapt_route(make_add_survey_controller())),
        methods=["POST"],
    )
    app.add_url_rule(
        "/api/surveys",
        "api_load_surveys",
        auth(adapt_route(make_load_surveys_controller())),
        methods=["GET"],
    )
