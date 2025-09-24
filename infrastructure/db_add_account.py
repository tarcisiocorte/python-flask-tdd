import uuid
from domain.usecases.add_account import AddAccount, AddAccountModel
from domain.models.account import AccountModel
from protocols.encrypter import Encrypter


class DbAddAccount(AddAccount):
    def __init__(self, encrypter: Encrypter):
        self.encrypter = encrypter
        # In a real application, this would be a database
        self.accounts = []
    
    async def add(self, account: AddAccountModel) -> AccountModel:
        await self.encrypter.encrypt(account.password)
        
        # Generate a unique ID for the account
        account_id = str(uuid.uuid4())
        
        # Create the account model
        new_account = AccountModel(
            id=account_id,
            name=account.name,
            email=account.email,
            password=account.password  # In production, this should be the hashed password
        )
        
        # Store the account (in memory for this example)
        self.accounts.append(new_account)
        
        return new_account
