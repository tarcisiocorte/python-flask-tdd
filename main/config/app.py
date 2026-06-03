"""Flask application factory and configuration."""
import os

from flask import Flask, request, jsonify
from data.usecases import DbAddAccount, DbAuthentication
from data.usecases.add_account.in_memory_add_account_repository import InMemoryAddAccountRepository
from infra.cryptography import JwtAdapter
from main.adapters import adapt_route
from main.config.middlewares import setup_middlewares
from presentation.controllers import LoginController
from presentation.controllers.signup.signup import SignUpController
from utils.bcrypt_encrypter import BcryptEncrypter
from utils.email_validator_adapter import EmailValidatorAdapter
from validation import (
    CompareFieldsValidation,
    EmailValidation,
    RequiredFieldValidation,
    ValidationComposite,
)


def create_app() -> Flask:
    app = Flask(__name__)
    setup_middlewares(app)

    account_repository = InMemoryAddAccountRepository()
    email_validator = EmailValidatorAdapter()
    bcrypt = BcryptEncrypter()
    add_account = DbAddAccount(bcrypt, account_repository, account_repository)
    authentication = DbAuthentication(
        account_repository,
        bcrypt,
        JwtAdapter(os.getenv("JWT_SECRET", "secret")),
        account_repository,
    )
    signup_validation = ValidationComposite([
        RequiredFieldValidation("name"),
        RequiredFieldValidation("email"),
        RequiredFieldValidation("password"),
        RequiredFieldValidation("passwordConfirmation"),
        CompareFieldsValidation("password", "passwordConfirmation"),
        EmailValidation("email", email_validator),
    ])
    signup_controller = SignUpController(add_account, signup_validation, authentication)
    login_validation = ValidationComposite([
        RequiredFieldValidation("email"),
        RequiredFieldValidation("password"),
        EmailValidation("email", email_validator),
    ])
    login_controller = LoginController(authentication, login_validation)

    @app.route("/signup", methods=["POST"])
    def legacy_signup():
        response, status_code = adapt_route(signup_controller)()
        data = response.get_json()
        if 200 <= status_code <= 299:
            return jsonify({"success": True, "data": data}), status_code
        return jsonify({"success": False, "error": data.get("error")}), status_code

    app.add_url_rule("/api/signup", "api_signup", adapt_route(signup_controller), methods=["POST"])
    app.add_url_rule("/api/login", "api_login", adapt_route(login_controller), methods=["POST"])

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app
