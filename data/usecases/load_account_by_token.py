from __future__ import annotations

from domain.models.account import AccountModel
from domain.usecases import LoadAccountByToken
from data.protocols import Decrypter, LoadAccountByTokenRepository


class DbLoadAccountByToken(LoadAccountByToken):
    def __init__(
        self,
        decrypter: Decrypter,
        load_account_by_token_repository: LoadAccountByTokenRepository,
    ):
        self.decrypter = decrypter
        self.load_account_by_token_repository = load_account_by_token_repository

    async def load(self, access_token: str, role: str | None = None) -> AccountModel | None:
        try:
            token = await self.decrypter.decrypt(access_token)
        except Exception:
            return None
        if token:
            return await self.load_account_by_token_repository.load_by_token(
                access_token, role
            )
        return None
