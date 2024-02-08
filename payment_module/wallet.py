from db import models
from db.database_manager import DatabaseManager
from users_module import personalized_exceptions
from payment_module import queryset


class Wallets:

    @staticmethod
    def get_wallet(user_id: int):
        r = queryset.get_wallet_query(user_id=user_id)

        if len(r) == 0:
            raise personalized_exceptions.WalletNotFound()
        r = models.wallet_model(r[0][0], r[0][1], r[0][2])
        return r

    @staticmethod
    def create_wallet(user_id: int):
        r = queryset.select_wallet_query(user_id=user_id)

        if r is not None and len(r) > 0:
            raise personalized_exceptions.CreateWalletError()

        queryset.add_wallet_query(user_id)

        return True

    @staticmethod
    def update_wallet(wallet: models.wallet_model):
        queryset.update_wallet(wallet.balance, wallet.id)

        return True

    @staticmethod
    def deposit_to_wallet(user_id: int, amount: float):
        wallet = Wallets.get_wallet(user_id)
        wallet.balance += amount
        Wallets.update_wallet(wallet)
        return True

    @staticmethod
    def harvest_from_wallet(user_id: int, amount: int):
        wallet = Wallets.get_wallet(user_id)
        if wallet.balance < amount:
            raise personalized_exceptions.NotEnoughBalance()
        wallet.balance -= amount
        Wallets.update_wallet(wallet)
        return True

    @staticmethod
    def get_balance(user_id):
        wallet = Wallets.get_wallet(user_id)
        return wallet.balance

# Users.AddUser(models.user_model(-1,'Masih1','masih@123.com','1990-10-10',None,'M@@@sih1',models.SubscriptopnType.Bronze.value))
# Wallets.create_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71')
# Wallets.get_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71')
# Wallets.harvest_from_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71',10)
# Wallets.deposit_to_wallet('dff5dd6b-ccfb-4123-85f3-ef39a5827e71',50000)
