import bcrypt
from datetime import datetime
from db import models
from db.database_manager import DatabaseManager
from users_module.users import UserInputValidator
import os
from users_module import personalized_exceptions
import transaction
from settings import local_settings
from payment_module import queryset


class BankAccounts:
    def __int__(self):
        self.log_file = local_settings.log_file

    @staticmethod
    def _hashPassword(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def cvv2_validator(cvv: int):
        if len(str(cvv)) > 4 or len(str(cvv)) < 3:
            raise personalized_exceptions.InvalidCvv2()

    def add_log(self, txt: str):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                pass
        with open(self.log_file, 'a') as f:
            f.write(
                txt +
                f""" _ at {
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""" +
                os.linesep)

    @staticmethod
    def add_bank_account(account: models.bank_account_model):
        UserInputValidator.password_validator(account.password)
        BankAccounts.cvv2_validator(account.cvv2)
        r = queryset.check_bank_account_query(account_userid=account.user_id, account_name=account.name)
        if r[0][0] != 0:
            raise personalized_exceptions.InvalidNameForBankAccount()
        data = {
            'user_id': account.user_id,
            'name': account.name,
            'balance': account.balance,
            'cvv2': account.cvv2,
            'password': BankAccounts._hashPassword(account.password),
        }
        queryset.add_bank_account_query(data)

        BankAccounts.add_log(
            f"Bank account created _ {
                account.user_id=} _ {
                account.name=}")

        return True

    @staticmethod
    def get_bank_accounts(user_id: str):
        r = queryset.get_bank_accounts_query(user_id=user_id)
        return r

    @staticmethod
    def get_bank_account_balance(
            user_id: str,
            account_name: str,
            cvv: int,
            password_account: str):

        r = queryset.get_bank_accounts_balance_query(user_id, account_name)
        if len(r) == 0:
            raise personalized_exceptions.BankAccountNotFound()

        if cvv != r[0][0] or not bcrypt.checkpw(
                password_account.encode('utf-8'),
                r[0][1].encode('utf-8')):
            raise personalized_exceptions.InvalidAccountSecurityInformation()

        return r[0][2] + " : " + str(r[0][3])

    @staticmethod
    def deposit_to_bank_account(
            user_id: str,
            account_name: str,
            amount: int) -> bool:

        r = queryset.deposit_to_bank_account_query(user_id, account_name)
        if len(r) == 0:
            raise personalized_exceptions.BankAccountNotFound()
        id_bank = r[0][0]
        balance = r[0][1]
        queryset.update_balance_query(id_bank, balance, amount)

        BankAccounts.add_log(
            f"Deposit _ {
                user_id=} _ {
                account_name=} _ {
                amount=}")

        return True

    @staticmethod
    def harvest_from_bank_account(
            user_id: str,
            cvv: int,
            password_account: str,
            amount: float,
            account_name: str) -> bool:

        r = queryset.harvest_from_account(account_name, user_id)

        if len(r) == 0:
            raise personalized_exceptions.BankAccountNotFound()

        account = models.bank_account_model(
            r[0][0], r[0][1], r[0][2], r[0][3], r[0][4], r[0][5])

        if cvv != account.cvv2 or not bcrypt.checkpw(
                password_account.encode('utf-8'), r[0][5].encode('utf-8')):
            raise personalized_exceptions.InvalidAccountSecurityInformation()
        if account.balance < amount:
            raise personalized_exceptions.NotEnoughBalance()

        queryset.update_new_balance_query(account.id, account.balance, amount)

        BankAccounts.add_log(
            f""""harvest _ {
                user_id=} _ {
                account_name=} _ {
                amount=}""")

        return True

    @staticmethod
    def money_transfer(
            user_id_origin: str,
            account_name_origin: str,
            cvv: int,
            password: str,
            user_id_destination: str,
            account_name_destination: str,
            amount: int):
        try:
            BankAccounts.harvest_from_bank_account(
                user_id_origin, cvv, password, amount, account_name_origin)

            BankAccounts.deposit_to_bank_account(
                user_id_destination, account_name_destination, amount)

            transaction.commit()

        except Exception as e:
            transaction.abort()
            return False
        return True

    @staticmethod
    def remove_bank_account(name):
        pass

    @staticmethod
    def show_all_accounts_by_username(username):
        pass




