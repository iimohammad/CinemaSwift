from db import models
from db.database_manager import DatabaseManager
import personalized_exceptions


class Wallets:
    """
    A class for managing wallet operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    database_manager = DatabaseManager()

    @staticmethod
    def _get_wallet(user_id: str):
        """
        Retrieves the wallet associated with a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            models.wallet_model: The wallet model.
        
        Raises:
            personalized_exceptions.WalletNotFound: If the wallet is not found.
        """
        query = f"SELECT * FROM wallets WHERE user_id = '{user_id}'"
        r = Wallets.database_manager.execute_query_select(query)
        if len(r) == 0:
            raise personalized_exceptions.WalletNotFound()
        r = models.wallet_model(r[0][0], r[0][1], r[0][2])
        return r

    @staticmethod
    def create_wallet(user_id: str):
        """
        Creates a new wallet for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if the wallet was created successfully, False otherwise.

        Raises:
            personalized_exceptions.CreateWalletError: If the wallet already exists.
        """
        query = f"SELECT id FROM wallets WHERE user_id = '{user_id}'"
        r = Wallets.database_manager.execute_query_select(query)
        if r is not None and len(r) > 0:
            raise personalized_exceptions.CreateWalletError()
        query = f"INSERT INTO wallets  (user_id, balance) VALUES ('{
            user_id}', 0);"
        Wallets.database_manager.execute_query(query)
        return True

    @staticmethod
    def _update_wallet(wallet: models.wallet_model):
        """
        Updates the balance of a wallet.

        Args:
            wallet (models.wallet_model): The wallet model.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = f"UPDATE `cinemaswift`.`wallets` SET `balance` = '{
            wallet.balance}' WHERE (`id` = '{wallet.id}');"
        Wallets.database_manager.execute_query(query)
        return True

    @staticmethod
    def deposit_to_wallet(user_id: int, amount: float):
        """
        Deposits money into a user's wallet.

        Args:
            user_id (int): The ID of the user.
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit was successful, False otherwise.
        """
        wallet = Wallets._get_wallet(user_id)
        wallet.balance += amount
        Wallets._update_wallet(wallet)
        return True

    @staticmethod
    def harvest_from_wallet(user_id: int, amount: int):
        """
        Withdraws money from a user's wallet.

        Args:
            user_id (int): The ID of the user.
            amount (int): The amount to withdraw.

        Returns:
            bool: True if the withdrawal was successful, False otherwise.

        Raises:
            personalized_exceptions.NotEnoughBalance: If the balance is insufficient.
        """
        wallet = Wallets._get_wallet(user_id)
        if wallet.balance < amount:
            raise personalized_exceptions.NotEnoughBalance()
        wallet.balance -= amount
        Wallets._update_wallet(wallet)
        return True

    @staticmethod
    def get_balance(user_id):
        """
        Retrieves the balance of a user's wallet.

        Args:
            user_id (str): The ID of the user.

        Returns:
            float: The balance of the wallet.
        """
        wallet = Wallets._get_wallet(user_id)
        return wallet.balance

# Users.AddUser(models.user_model(-1,'Masih1','masih@123.com','1990-10-10',None,'M@@@sih1',models.SubscriptopnType.Bronze.value))
# Wallets.create_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71')
# Wallets.get_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71')
# Wallets.harvest_from_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71',10)
# Wallets.deposit_to_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71',50000)
