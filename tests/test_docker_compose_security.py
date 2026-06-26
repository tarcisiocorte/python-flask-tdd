from pathlib import Path

import yaml


def _compose() -> dict:
    return yaml.safe_load(Path("docker-compose.yml").read_text())


def test_database_services_do_not_publish_host_ports():
    services = _compose()["services"]

    assert "ports" not in services["mongodb"]
    assert "ports" not in services["postgres"]


def test_api_uses_mongodb_application_credentials_not_root_credentials():
    api_environment = _compose()["services"]["api"]["environment"]

    assert "MONGO_APP_USER" in api_environment["MONGO_URL"]
    assert "MONGO_APP_PASSWORD" in api_environment["MONGO_URL"]
    assert "MONGO_ROOT_USER" not in api_environment["MONGO_URL"]
    assert "MONGO_ROOT_PASSWORD" not in api_environment["MONGO_URL"]
