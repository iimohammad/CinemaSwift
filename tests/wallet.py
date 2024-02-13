import unittest
from unittest.mock import MagicMock
from payment_module.wallet import Wallets
from users_module import personalized_exceptions

class TestWallets(unittest.TestCase):

    def setUp(self):
        self.queryset = MagicMock()
        self.wallet_model = MagicMock()
        self.queryset.get_wallet_query.return_value = [(1, 100.0, 'user_id')]

    def test_get_wallet(self):
        wallet = Wallets.get_wallet('user_id')
        self.assertEqual(wallet.id, 1)
        self.assertEqual(wallet.balance, 100.0)

    def test_create_wallet(self):
        self.queryset.select_wallet_query.return_value = []
        self.assertTrue(Wallets.create_wallet('user_id'))

        self.queryset.select_wallet_query.return_value = [(1, 100.0, 'user_id')]
        with self.assertRaises(personalized_exceptions.CreateWalletError):
            Wallets.create_wallet('user_id')

    def test_deposit_to_wallet(self):
        wallet = MagicMock()
        wallet.balance = 100.0
        self.wallet_model.return_value = wallet

        Wallets.deposit_to_wallet('user_id', 50.0)
        self.assertEqual(wallet.balance, 150.0)

    def test_harvest_from_wallet(self):
        wallet = MagicMock()
        wallet.balance = 100.0
        self.wallet_model.return_value = wallet

        Wallets.harvest_from_wallet('user_id', 50.0)
        self.assertEqual(wallet.balance, 50.0)

        with self.assertRaises(personalized_exceptions.NotEnoughBalance):
            Wallets.harvest_from_wallet('user_id', 150.0)

if __name__ == '__main__':
    unittest.main()
