from db import models
from users import BaseForUsersAndAdmins
import os

class BankAccounts:
    log_file = 'transaction.log'
    @staticmethod
    def add_log(txt:str):
        if not os.path.exists(BankAccounts.log_file):
            with open(BankAccounts.log_file,'w'):
                pass
        with open(BankAccounts.log_file,'r') as f:
            f.write(txt)
            f.write(os.linesep)
            
    @staticmethod
    def add_bank_account(account:models.bank_accounts_models):
        if not BaseForUsersAndAdmins.PasswordValidator(account.password):
            return False
        if len(account.cvv2)!=4:
            return False
        
        accounts = BankAccounts.get_bank_accounts(account.user_id)
        for i in accounts:
            if i.name == account.name:
                return False
        
        # add to databalse
        
        return True
    
    @staticmethod
    def get_bank_accounts(user_id:str):
        r = []
        # r = user bank accounts id
        return r
    
    @staticmethod
    def get_bank_account(bank_account_id:int)->models.bank_accounts_models:
        r = models.bank_accounts_models(0,0,10,"g",1234,1234)
        # get account balance
        return r
    @staticmethod
    def update_bank_account(bank_account:models.bank_accounts_models)->bool:
        # update query
        return True
        
    @staticmethod
    def deposit_to_bank_account(amount:float,bank_account_id)->bool:
        ba = BankAccounts.get_bank_account(bank_account_id)
        ba.balance +=amount
        # deposit
        BankAccounts.add_log(f"deposit to {bank_account_id = }_{amount = } ")
        return True
    
    @staticmethod
    def harvest_from_bank_account(amount:float,bank_account_id)->bool:
        BankAccounts.add_log(f"harvest from {bank_account_id = }_{amount = } ")
        # harvest
        pass
    
    @staticmethod
    def money_transfer(amount:float, origin_bank_account_id:int , destination_bank_account_id):
        if not BankAccounts.harvest_from_bank_account(amount,origin_bank_account_id):
            return False
        BankAccounts.deposit_to_bank_account(amount,destination_bank_account_id)
        BankAccounts.add_log(f"transfer from {origin_bank_account_id = } _to_ {destination_bank_account_id = } _ {amount = }")
        return True