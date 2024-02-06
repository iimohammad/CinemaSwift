import bcrypt
from datetime import datetime
from db import models
from db.database_manager import DatabaseManager
from users import BaseForUsersAndAdmins
import os
import personalized_exceptions


class BankAccounts:
    """
    A class for managing bank account operations.

    Attributes:
        log_file (str): Path to the transaction log file.
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    log_file = 'transaction.log'
    database_manager = DatabaseManager()

    @staticmethod
    def _hashPassword(password: str):
        """
        Hashes the given password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def cvv2_validator(cvv: int):
        """
        Validates the CVV2 number.

        Args:
            cvv (int): The CVV2 number.

        Raises:
            personalized_exceptions.InvalidCvv2: If the CVV2 number is invalid.
        """
        if len(str(cvv)) > 4 or len(str(cvv)) < 3:
            raise personalized_exceptions.InvalidCvv2()

    @staticmethod
    def add_log(txt: str):
        """
        Adds a log entry to the transaction log file.

        Args:
            txt (str): The log entry to add.
        """
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
        """
        Adds a bank account to the database.

        Args:
            account (models.bank_account_model): The bank account to add.

        Returns:
            bool: True if the bank account was added successfully, False otherwise.
        """
        BaseForUsersAndAdmins.PasswordValidator(account.password)
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
        """
        Retrieves bank accounts associated with a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of bank account names.
        """
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
        """
        Retrieves the balance of a bank account.

        Args:
            user_id (str): The ID of the user.
            account_name (str): The name of the bank account.
            cvv (int): The CVV2 number.
            password_account (str): The password of the bank account.

        Returns:
            str: A string representing the account name and balance.
        """
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
        """
        Deposits money into a bank account.

        Args:
            user_id (str): The ID of the user.
            account_name (str): The name of the bank account.
            amount (int): The amount to deposit.

        Returns:
            bool: True if the deposit was successful, False otherwise.
        """
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
        """
        Withdraws money from a bank account.

        Args:
            user_id (str): The ID of the user.
            cvv (int): The CVV2 number.
            password_account (str): The password of the bank account.
            amount (float): The amount to withdraw.
            account_name (str): The name of the bank account.

        Returns:
            bool: True if the withdrawal was successful, False otherwise.
        """
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
        """
        Transfers money between bank accounts.

        Args:
            user_id_origin (str): The ID of the user initiating the transfer.
            account_name_origin (str): The name of the origin bank account.
            cvv (int): The CVV2 number of the origin bank account.
            password (str): The password of the origin bank account.
            user_id_destination (str): The ID of the user receiving the transfer.
            account_name_destination (str): The name of the destination bank account.
            amount (int): The amount to transfer.

        Returns:
            bool: True if the transfer was successful, False otherwise.
        """
        BankAccounts.harvest_from_bank_account(
            user_id_origin, cvv, password, amount, account_name_origin)

        BankAccounts.deposit_to_bank_account(
            user_id_destination, account_name_destination, amount)

        return True
