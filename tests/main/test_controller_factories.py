from data.usecases.add_account.db_add_account import DbAddAccount
from infra.db.mongodb import AccountMongoRepository
from main.factories.controllers import make_signup_controller


def test_signup_factory_uses_mongo_repository_for_add_and_duplicate_check():
    controller = make_signup_controller()

    add_account = controller.add_account

    assert isinstance(add_account, DbAddAccount)
    assert isinstance(add_account.add_account_repository, AccountMongoRepository)
    assert add_account.check_account_by_email_repository is (
        add_account.add_account_repository
    )
