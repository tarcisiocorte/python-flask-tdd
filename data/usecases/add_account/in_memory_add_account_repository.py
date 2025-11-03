import uuid
from data.protocols.add_account_repository import AddAccountRepository
from domain.usecases.add_account import AddAccountModel
from domain.models.account import AccountModel


class InMemoryAddAccountRepository(AddAccountRepository):
    def __init__(self):
        # In a real application, this would be a database
        self.accounts = []
    
    async def add(self, account: AddAccountModel) -> AccountModel:
        # Generate a unique ID for the account
        account_id = str(uuid.uuid4())
        
        # Create the account model
        new_account = AccountModel(
            id=account_id,
            name=account.name,
            email=account.email,
            password=account.password  # In production, this should be hashed
        )
        
        # Store the account (in memory for this example)
        self.accounts.append(new_account)
        
        return new_account

