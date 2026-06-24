from unittest.mock import Mock

import pytest

from main.config.app import create_app
from presentation.protocols import HttpResponse


@pytest.fixture
def controller_factories(monkeypatch):
    controllers = {
        "signup": Mock(),
        "login": Mock(),
        "add_survey": Mock(),
        "load_surveys": Mock(),
        "save_survey_result": Mock(),
        "load_survey_result": Mock(),
    }
    for controller in controllers.values():
        controller.handle.return_value = HttpResponse(200, {"ok": True})

    monkeypatch.setattr(
        "main.routes.login_routes.make_signup_controller",
        Mock(return_value=controllers["signup"]),
    )
    monkeypatch.setattr(
        "main.routes.login_routes.make_login_controller",
        Mock(return_value=controllers["login"]),
    )
    monkeypatch.setattr(
        "main.routes.survey_routes.make_add_survey_controller",
        Mock(return_value=controllers["add_survey"]),
    )
    monkeypatch.setattr(
        "main.routes.survey_routes.make_load_surveys_controller",
        Mock(return_value=controllers["load_surveys"]),
    )
    monkeypatch.setattr(
        "main.routes.survey_result_routes.make_save_survey_result_controller",
        Mock(return_value=controllers["save_survey_result"]),
    )
    monkeypatch.setattr(
        "main.routes.survey_result_routes.make_load_survey_result_controller",
        Mock(return_value=controllers["load_survey_result"]),
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
    return controllers


@pytest.fixture
def client(controller_factories):
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize(
    ("method", "path", "controller_name"),
    [
        ("post", "/api/signup", "signup"),
        ("post", "/api/login", "login"),
        ("post", "/api/surveys", "add_survey"),
        ("get", "/api/surveys", "load_surveys"),
        ("put", "/api/surveys/survey-123/results", "save_survey_result"),
        ("get", "/api/surveys/survey-123/results", "load_survey_result"),
    ],
)
def test_registers_all_api_routes(
    client,
    controller_factories,
    method,
    path,
    controller_name,
):
    response = getattr(client, method)(path, json={"answer": "yes"})

    assert response.status_code == 200
    controller_factories[controller_name].handle.assert_called_once()


@pytest.mark.parametrize(
    "controller_name",
    ["save_survey_result", "load_survey_result"],
)
def test_passes_flask_route_params_to_http_request(
    client,
    controller_factories,
    controller_name,
):
    method = "put" if controller_name == "save_survey_result" else "get"

    getattr(client, method)("/api/surveys/survey-123/results", json={"answer": "yes"})

    http_request = controller_factories[controller_name].handle.call_args.args[0]
    assert http_request.params == {"survey_id": "survey-123"}


def test_keeps_legacy_signup_route(client, controller_factories):
    response = client.post("/signup", json={"name": "Legacy User"})

    assert response.status_code == 200
    assert response.get_json() == {"success": True, "data": {"ok": True}}
    controller_factories["signup"].handle.assert_called_once()


class TokenAuthMiddleware:
    def __init__(self, role=None):
        self.role = role

    def handle(self, http_request):
        token = http_request.headers.get("x-access-token")
        if not token or (self.role == "admin" and token != "admin-token"):
            return HttpResponse(403, Exception("Access denied"))
        return HttpResponse(
            200,
            {"account_id": f"{token}-account", "accountId": f"{token}-account"},
        )


@pytest.fixture
def auth_client(monkeypatch, controller_factories):
    auth_factory = Mock(side_effect=lambda role=None: TokenAuthMiddleware(role))
    monkeypatch.setattr(
        "main.routes.survey_routes.make_auth_middleware",
        auth_factory,
    )
    monkeypatch.setattr(
        "main.routes.survey_result_routes.make_auth_middleware",
        auth_factory,
    )
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client(), controller_factories, auth_factory


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("post", "/api/surveys"),
        ("get", "/api/surveys"),
        ("put", "/api/surveys/survey-123/results"),
        ("get", "/api/surveys/survey-123/results"),
    ],
)
def test_protected_routes_reject_anonymous_requests(auth_client, method, path):
    client, _, _ = auth_client

    response = getattr(client, method)(path, json={"answer": "yes"})

    assert response.status_code == 403
    assert response.get_json() == {"error": "Access denied"}


def test_add_survey_requires_admin_role(auth_client):
    client, controllers, auth_factory = auth_client

    user_response = client.post(
        "/api/surveys",
        headers={"x-access-token": "user-token"},
        json={"question": "Question"},
    )
    admin_response = client.post(
        "/api/surveys",
        headers={"x-access-token": "admin-token"},
        json={"question": "Question"},
    )

    assert user_response.status_code == 403
    assert admin_response.status_code == 200
    controllers["add_survey"].handle.assert_called_once()
    auth_factory.assert_any_call("admin")


@pytest.mark.parametrize(
    ("method", "path", "controller_name"),
    [
        ("get", "/api/surveys", "load_surveys"),
        ("put", "/api/surveys/survey-123/results", "save_survey_result"),
        ("get", "/api/surveys/survey-123/results", "load_survey_result"),
    ],
)
def test_user_token_can_access_user_routes(
    auth_client,
    method,
    path,
    controller_name,
):
    client, controllers, auth_factory = auth_client

    response = getattr(client, method)(
        path,
        headers={"x-access-token": "user-token"},
        json={"answer": "yes"},
    )

    assert response.status_code == 200
    http_request = controllers[controller_name].handle.call_args.args[0]
    assert http_request.account_id == "user-token-account"
    auth_factory.assert_any_call()
