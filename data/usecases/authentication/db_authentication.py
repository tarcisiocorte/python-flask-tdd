from __future__ import annotations

from domain.usecases import Authentication, AuthenticationModel, AuthenticationParams
from data.protocols import (
    Encrypter,
    HashComparer,
    LoadAccountByEmailRepository,
    UpdateAccessTokenRepository,
)


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repository: LoadAccountByEmailRepository,
        hash_comparer: HashComparer,
        encrypter: Encrypter,
        update_access_token_repository: UpdateAccessTokenRepository,
    ):
        self.load_account_by_email_repository = load_account_by_email_repository
        self.hash_comparer = hash_comparer
        self.encrypter = encrypter
        self.update_access_token_repository = update_access_token_repository

    async def auth(
        self, params: AuthenticationParams | dict[str, str]
    ) -> AuthenticationModel | None:
        email = params["email"] if isinstance(params, dict) else params.email
        password = params["password"] if isinstance(params, dict) else params.password
        account = await self.load_account_by_email_repository.load_by_email(email)
        if account:
            is_valid = await self.hash_comparer.compare(password, account.password)
            if is_valid:
                access_token = await self.encrypter.encrypt(account.id)
                await self.update_access_token_repository.update_access_token(
                    account.id, access_token
                )
                return AuthenticationModel(access_token=access_token, name=account.name)
        return None
