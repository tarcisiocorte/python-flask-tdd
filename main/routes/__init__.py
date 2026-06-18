"""Flask route registration modules."""

from main.routes.login_routes import register_login_routes
from main.routes.survey_result_routes import register_survey_result_routes
from main.routes.survey_routes import register_survey_routes

__all__ = [
    "register_login_routes",
    "register_survey_result_routes",
    "register_survey_routes",
]
