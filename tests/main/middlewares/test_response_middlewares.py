from flask import jsonify

from main.config.app import create_app


def test_adds_json_content_type_and_cross_origin_headers():
    app = create_app()
    app.config["TESTING"] = True

    @app.get("/test-response-headers")
    def test_response_headers():
        return jsonify({"ok": True})

    response = app.test_client().get("/test-response-headers")

    assert response.content_type == "application/json"
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert response.headers["Access-Control-Allow-Methods"] == "GET,POST,PUT,DELETE,OPTIONS"
    assert (
        response.headers["Access-Control-Allow-Headers"]
        == "Content-Type,Authorization,x-access-token"
    )


def test_adds_no_cache_headers():
    response = create_app().test_client().get("/health")

    assert (
        response.headers["Cache-Control"]
        == "no-store, no-cache, must-revalidate, proxy-revalidate"
    )
    assert response.headers["Pragma"] == "no-cache"
    assert response.headers["Expires"] == "0"
    assert response.headers["Surrogate-Control"] == "no-store"


def test_handles_options_preflight_without_authentication(monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "https://example.com")
    monkeypatch.setenv("CORS_ALLOWED_METHODS", "GET,POST")
    monkeypatch.setenv("CORS_ALLOWED_HEADERS", "Content-Type,x-access-token")

    response = create_app().test_client().options(
        "/api/surveys",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 204
    assert response.data == b""
    assert response.headers["Access-Control-Allow-Origin"] == "https://example.com"
    assert response.headers["Access-Control-Allow-Methods"] == "GET,POST"
    assert response.headers["Access-Control-Allow-Headers"] == "Content-Type,x-access-token"


def test_does_not_force_json_content_type_on_empty_204_response():
    app = create_app()

    @app.get("/test-no-content")
    def no_content():
        return "", 204

    response = app.test_client().get("/test-no-content")

    assert response.status_code == 204
    assert response.data == b""
    assert response.content_type != "application/json"
