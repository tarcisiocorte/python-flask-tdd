from unittest.mock import Mock

import pytest

from domain.usecases import AuthenticationModel
from main.config.app import create_app
from presentation.errors import UnauthorizedError
from presentation.protocols import HttpResponse


@pytest.fixture
def client(monkeypatch):
    signup_controller = Mock()
    signup_controller.handle.return_value = HttpResponse(
        200,
        AuthenticationModel(access_token="signup_token", name="Signup User"),
    )
    login_controller = Mock()
    login_controller.handle.return_value = HttpResponse(
        200,
        AuthenticationModel(access_token="login_token", name="Login User"),
    )
    monkeypatch.setattr(
        "main.routes.login_routes.make_signup_controller",
        Mock(return_value=signup_controller),
    )
    monkeypatch.setattr(
        "main.routes.login_routes.make_login_controller",
        Mock(return_value=login_controller),
    )
    auth_middleware = Mock()
    auth_middleware.handle.return_value = HttpResponse(
        200,
        {"account_id": "account-123", "accountId": "account-123"},
    )
    monkeypatch.setattr(
        "main.routes.survey_routes.make_auth_middleware",
        Mock(return_value=auth_middleware),
    )
    monkeypatch.setattr(
        "main.routes.survey_result_routes.make_auth_middleware",
        Mock(return_value=auth_middleware),
    )
    for route_module, factory_name in [
        ("main.routes.survey_routes", "make_add_survey_controller"),
        ("main.routes.survey_routes", "make_load_surveys_controller"),
        ("main.routes.survey_result_routes", "make_save_survey_result_controller"),
        ("main.routes.survey_result_routes", "make_load_survey_result_controller"),
    ]:
        controller = Mock()
        controller.handle.return_value = HttpResponse(200, {"ok": True})
        monkeypatch.setattr(
            f"{route_module}.{factory_name}",
            Mock(return_value=controller),
        )
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client(), signup_controller, login_controller


def test_signup_returns_public_authentication_contract(client):
    test_client, signup_controller, _ = client

    response = test_client.post(
        "/api/signup",
        json={
            "name": "Signup User",
            "email": "signup@mail.com",
            "password": "Valid_secret123",
            "passwordConfirmation": "Valid_secret123",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "accessToken": "signup_token",
        "name": "Signup User",
    }
    signup_controller.handle.assert_called_once()


def test_login_returns_public_authentication_contract(client):
    test_client, _, login_controller = client

    response = test_client.post(
        "/api/login",
        json={"email": "login@mail.com", "password": "secret"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "accessToken": "login_token",
        "name": "Login User",
    }
    login_controller.handle.assert_called_once()


def test_login_returns_401_for_invalid_credentials(client):
    test_client, _, login_controller = client
    login_controller.handle.return_value = HttpResponse(401, UnauthorizedError())

    response = test_client.post(
        "/api/login",
        json={"email": "login@mail.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}


def test_login_is_rate_limited(monkeypatch, client):
    monkeypatch.setenv("AUTH_RATE_LIMIT_MAX_REQUESTS", "2")
    monkeypatch.setenv("AUTH_RATE_LIMIT_WINDOW_SECONDS", "60")
    test_client, _, login_controller = client

    for _ in range(2):
        response = test_client.post(
            "/api/login",
            json={"email": "login@mail.com", "password": "Valid_secret123"},
        )
        assert response.status_code == 200

    response = test_client.post(
        "/api/login",
        json={"email": "login@mail.com", "password": "Valid_secret123"},
    )

    assert response.status_code == 429
    assert response.get_json() == {"error": "Too many requests"}
    assert login_controller.handle.call_count == 2
