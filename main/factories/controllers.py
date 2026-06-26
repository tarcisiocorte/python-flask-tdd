import os

from data.usecases import (
    DbAddAccount,
    DbAddSurvey,
    DbAuthentication,
    DbCheckSurveyById,
    DbLoadAnswersBySurvey,
    DbLoadSurveyResult,
    DbLoadSurveys,
    DbSaveSurveyResult,
)
from infra.cryptography import BcryptAdapter, JwtAdapter
from infra.db.mongodb import (
    AccountMongoRepository,
    SurveyMongoRepository,
    SurveyResultMongoRepository,
)
from main.config.env import jwt_secret
from presentation.controllers import (
    AddSurveyController,
    LoadSurveyResultController,
    LoadSurveysController,
    LoginController,
    SaveSurveyResultController,
    SignUpController,
)
from utils.email_validator_adapter import EmailValidatorAdapter
from validation import (
    CompareFieldsValidation,
    EmailValidation,
    PasswordStrengthValidation,
    RequiredFieldValidation,
    ValidationComposite,
)

def make_signup_validation():
    email_validator = EmailValidatorAdapter()
    return ValidationComposite([
        RequiredFieldValidation("name"),
        RequiredFieldValidation("email"),
        RequiredFieldValidation("password"),
        RequiredFieldValidation("passwordConfirmation"),
        CompareFieldsValidation("password", "passwordConfirmation"),
        PasswordStrengthValidation("password"),
        EmailValidation("email", email_validator),
    ])


def make_login_validation():
    email_validator = EmailValidatorAdapter()
    return ValidationComposite([
        RequiredFieldValidation("email"),
        RequiredFieldValidation("password"),
        EmailValidation("email", email_validator),
    ])


def make_add_survey_validation():
    return ValidationComposite([
        RequiredFieldValidation("question"),
        RequiredFieldValidation("answers"),
    ])


def make_account_repository():
    return AccountMongoRepository()


def make_survey_repository():
    return SurveyMongoRepository()


def make_survey_result_repository():
    return SurveyResultMongoRepository()


def make_authentication():
    account_repository = make_account_repository()
    bcrypt_adapter = BcryptAdapter(int(os.getenv("BCRYPT_SALT", "12")))
    jwt_adapter = JwtAdapter(jwt_secret())
    return DbAuthentication(
        account_repository,
        bcrypt_adapter,
        jwt_adapter,
        account_repository,
    )


def make_signup_controller():
    account_repository = make_account_repository()
    add_account = DbAddAccount(
        BcryptAdapter(int(os.getenv("BCRYPT_SALT", "12"))),
        account_repository,
        account_repository,
    )
    return SignUpController(add_account, make_signup_validation(), make_authentication())


def make_login_controller():
    return LoginController(make_authentication(), make_login_validation())


def make_add_survey_controller():
    return AddSurveyController(make_add_survey_validation(), DbAddSurvey(make_survey_repository()))


def make_load_surveys_controller():
    return LoadSurveysController(DbLoadSurveys(make_survey_repository()))


def make_save_survey_result_controller():
    survey_repository = make_survey_repository()
    survey_result_repository = make_survey_result_repository()
    return SaveSurveyResultController(
        DbLoadAnswersBySurvey(survey_repository),
        DbSaveSurveyResult(survey_result_repository, survey_result_repository),
    )


def make_load_survey_result_controller():
    survey_repository = make_survey_repository()
    survey_result_repository = make_survey_result_repository()
    return LoadSurveyResultController(
        DbCheckSurveyById(survey_repository),
        DbLoadSurveyResult(survey_result_repository, survey_repository),
    )
