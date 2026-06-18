"""Signup and login route registration."""

from flask import Flask, jsonify

from main.adapters import adapt_route
from main.factories.controllers import make_login_controller, make_signup_controller


def register_login_routes(app: Flask) -> None:
    """Register account routes, including the backwards-compatible signup route."""
    signup_controller = make_signup_controller()
    login_controller = make_login_controller()
    signup_route = adapt_route(signup_controller)

    app.add_url_rule(
        "/api/signup",
        "api_signup",
        signup_route,
        methods=["POST"],
    )
    app.add_url_rule(
        "/api/login",
        "api_login",
        adapt_route(login_controller),
        methods=["POST"],
    )

    def legacy_signup():
        response, status_code = signup_route()
        data = response.get_json()
        if 200 <= status_code <= 299:
            return jsonify({"success": True, "data": data}), status_code
        return jsonify({"success": False, "error": data.get("error")}), status_code

    app.add_url_rule(
        "/signup",
        "legacy_signup",
        legacy_signup,
        methods=["POST"],
    )
