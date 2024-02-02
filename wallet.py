from db import models
class Wallets:
    @staticmethod
    def get_wallet(user_id:str):
        r = models.wallet_model(0,10,"asdasd")
        
        # query : get_wallet
        
        return r
    
    @staticmethod
    def create_wallet(user_id:str):
        # query : each user only have one wallet
        wallet = models.wallet_model(user_id)
        # query : add wallet
        return True
    
    @staticmethod
    def _update_wallet(wallet:models.wallets_model):
        # query : update wallet
        return True
    
    @staticmethod
    def deposit_to_wallet(user_id:int,amount:float):
        wallet = Wallets.get_wallet(user_id)
        wallet.balance += amount
        Wallets._update_wallet(wallet)
        return True
    
    @staticmethod
    def harvest_from_wallet(user_id:int,amount:float):
        wallet = Wallets.get_wallet(user_id)
        wallet.balance -= amount
        Wallets._update_wallet(wallet)
        return True