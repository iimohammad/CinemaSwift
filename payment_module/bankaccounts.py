import bcrypt
from datetime import datetime
from db import models
from db.database_manager import DatabaseManager
from users import BaseForUsersAndAdmins
import os
from users_module import personalized_exceptions


class BankAccounts:

    log_file = 'transaction.log'
    database_manager = DatabaseManager()

    @staticmethod
    def _hashPassword(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def cvv2_validator(cvv: int):
        if len(str(cvv)) > 4 or len(str(cvv)) < 3:
            raise personalized_exceptions.InvalidCvv2()

    @staticmethod
    def add_log(txt: str):
        if not os.path.exists(BankAccounts.log_file):
            with open(BankAccounts.log_file, 'w') as f:
                pass
        with open(BankAccounts.log_file, 'a') as f:
            f.write(
                txt +
                f" _ at {
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" +
                os.linesep)

    @staticmethod
    def add_bank_account(account: models.bank_account_model):

        BaseForUsersAndAdmins.password_validator(account.password)
        BankAccounts.cvv2_validator(account.cvv2)
        query = f"""SELECT count(id) FROM cinemaswift.bankaccounts
                WHERE
                user_id = '{account.user_id}' AND name = '{account.name}'; """
        r = BankAccounts.database_manager.execute_query_select(query)
        if r[0][0] != 0:
            raise personalized_exceptions.InvalidNameForBankAccount()
        data = {
            'user_id': account.user_id,
            'name': account.name,
            'balance': account.balance,
            'cvv2': account.cvv2,
            'password': BankAccounts._hashPassword(account.password),
        }
        query = """INSERT INTO `cinemaswift`.`bankaccounts` (`user_id`, `name`, `balance`, `cvv2`, `password`)
                VALUES
                (%(user_id)s, %(name)s, %(balance)s, %(cvv2)s, %(password)s);"""
        BankAccounts.database_manager.execute_query(query, data)

        BankAccounts.add_log(
            f"Bank account created _ {
                account.user_id=} _ {
                account.name=}")

        return True

    @staticmethod
    def get_bank_accounts(user_id: str):
        query = f"""SELECT name FROM cinemaswift.bankaccounts
                WHERE
                user_id = '{user_id}';"""
        r = BankAccounts.database_manager.execute_query_select(query)
        return r

    @staticmethod
    def get_bank_account_balance(
            user_id: str,
            account_name: str,
            cvv: int,
            password_account: str):
        query = f"""SELECT cvv2,password,name,balance FROM cinemaswift.bankaccounts
                WHERE user_id = '{user_id}' AND name = '{account_name}';"""

        r = BankAccounts.database_manager.execute_query_select(query)

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
        query = f"""SELECT id,balance FROM cinemaswift.bankaccounts
                WHERE
                user_id = '{user_id}' AND name = '{account_name}';"""
        r = BankAccounts.database_manager.execute_query_select(query)
        if len(r) == 0:
            raise personalized_exceptions.BankAccountNotFound()
        id = r[0][0]
        balance = r[0][1]
        query = f"""UPDATE `cinemaswift`.`bankaccounts` SET `balance` = '{
            balance + amount}' WHERE (`id` = '{id}');"""
        BankAccounts.database_manager.execute_query(query)

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

        query = f"""SELECT * FROM cinemaswift.bankaccounts
                WHERE user_id = '{user_id}' AND name = '{account_name}';"""
        r = BankAccounts.database_manager.execute_query_select(query)
        if len(r) == 0:
            raise personalized_exceptions.BankAccountNotFound()

        account = models.bank_account_model(
            r[0][0], r[0][1], r[0][2], r[0][3], r[0][4], r[0][5])

        if cvv != account.cvv2 or not bcrypt.checkpw(
                password_account.encode('utf-8'), r[0][5].encode('utf-8')):
            raise personalized_exceptions.InvalidAccountSecurityInformation()
        if account.balance < amount:
            raise personalized_exceptions.NotEnoughBalance()

        query = f"""UPDATE `cinemaswift`.`bankaccounts` SET `balance` = '{
            account.balance - amount}'
                WHERE
                (`id` = '{account.id}');"""
        BankAccounts.database_manager.execute_query(query)

        BankAccounts.add_log(
            f"harvest _ {
                user_id=} _ {
                account_name=} _ {
                amount=}")

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

        BankAccounts.harvest_from_bank_account(
            user_id_origin, cvv, password, amount, account_name_origin)

        BankAccounts.deposit_to_bank_account(
            user_id_destination, account_name_destination, amount)

        return True
