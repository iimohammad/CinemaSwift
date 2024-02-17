from db import models
from db.database_manager import DatabaseManager
from users_module import personalized_exceptions
from payment_module import queryset
import os
from datetime import datetime

class Wallets:
    log_file = "wallets.log"
    @classmethod
    def add_log(cls,txt: str):
        if not os.path.exists(cls.log_file):
            with open(cls.log_file, 'w') as f:
                pass
        with open(cls.log_file, 'a') as f:
            f.write(
                txt +
                f""" _ at {
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""" +
                os.linesep)
    @staticmethod
    def get_wallet(user_id: str):
        r = queryset.get_wallet_query(user_id=user_id)
        if len(r) == 0:
            raise personalized_exceptions.WalletNotFound()
        r = models.wallet_model(r[0][0], r[0][1], r[0][2])
        return r

    @staticmethod
    def create_wallet(user_id: str):
        r = queryset.select_wallet_query(user_id=user_id)

        if r is not None and len(r) > 0:
            raise personalized_exceptions.CreateWalletError()

        queryset.add_wallet_query(user_id)
        Wallets.add_log(f"""Wallet created _ {user_id = }""")
        return True

    @staticmethod
    def update_wallet(wallet: models.wallet_model):
        queryset.update_wallet(wallet.balance, wallet.id)

        return True

    @staticmethod
    def deposit_to_wallet(user_id: str, amount: float):
        wallet = Wallets.get_wallet(user_id)
        wallet.balance += amount
        Wallets.update_wallet(wallet)
        Wallets.add_log(f"""Deposit to Wallet _ {user_id = } _ {amount = }""")
        return True

    @staticmethod
    def harvest_from_wallet(user_id: str, amount: int):
        wallet = Wallets.get_wallet(user_id)
        if wallet.balance < amount:
            raise personalized_exceptions.NotEnoughBalance()
        wallet.balance -= amount
        Wallets.update_wallet(wallet)
        Wallets.add_log(f"""Harvers from Wallet _ {user_id = } _ {amount = }""")
        return True

    @staticmethod
    def get_balance(user_id : str):
        wallet = Wallets.get_wallet(user_id)
        return wallet.balance
