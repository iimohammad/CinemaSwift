import unittest
from payment_module.queryset import *

class TestDatabaseFunctions(unittest.TestCase):
    def test_check_bank_account_query(self):
        mock_account_userid = '123456'
        mock_account_name = 'mock_account'
        result = check_bank_account_query(mock_account_userid, mock_account_name)
        self.assertEqual(result, 1)

    def test_add_bank_account_query(self):
        mock_data = {
            'user_id': '123456',
            'name': 'mock_account',
            'balance': 100,
            'cvv2': '123',
            'password': 'password123'
        }
        add_bank_account_query(mock_data)
        result = get_bank_accounts_query(mock_data['user_id'])
        self.assertIn(mock_data['name'], [item['name'] for item in result])

    def test_get_bank_accounts_balance_query(self):
        mock_user_id = '123456'
        mock_account_name = 'mock_account'
        result = get_bank_accounts_balance_query(mock_user_id, mock_account_name)
        self.assertTrue(isinstance(result['balance'], int))
        self.assertTrue(result['balance'] >= 0)

    def test_deposit_to_bank_account_query(self):
        mock_user_id = '123456'
        mock_account_name = 'mock_account'
        result = deposit_to_bank_account_query(mock_user_id, mock_account_name)
        self.assertTrue('id' in result and 'balance' in result)

    def test_update_balance_query(self):
        mock_id_bank = '123'
        mock_balance = 100
        mock_amount = 50
        update_balance_query(mock_id_bank, mock_balance, mock_amount)
        updated_result = get_bank_accounts_balance_query(mock_id_bank)
        self.assertEqual(updated_result['balance'], mock_balance + mock_amount)

    def test_harvest_from_account(self):
        mock_user_id = '123456'
        mock_account_name = 'mock_account'
        result = harvest_from_account(mock_account_name, mock_user_id)
        self.assertTrue(result)

    def test_update_new_balance_query(self):
        mock_id = '123'
        mock_balance = 100
        mock_amount = 50
        update_new_balance_query(mock_id, mock_balance, mock_amount)
        updated_result = get_bank_accounts_balance_query(mock_id)
        self.assertEqual(updated_result['balance'], mock_balance - mock_amount)

    def test_get_wallet_query(self):
        mock_user_id = '123456'
        result = get_wallet_query(mock_user_id)
        self.assertTrue(result)

    def test_select_wallet_query(self):
        mock_user_id = '123456'
        result = select_wallet_query(mock_user_id)
        self.assertTrue(result)

    def test_add_wallet_query(self):
        mock_user_id = '123456'
        add_wallet_query(mock_user_id)
        result = get_wallet_query(mock_user_id)
        self.assertTrue(result)

    def test_update_wallet(self):
        mock_balance = 100
        mock_wallet_id = '123'
        update_wallet(mock_balance, mock_wallet_id)
        updated_result = get_wallet_query(mock_wallet_id)
        self.assertEqual(updated_result['balance'], mock_balance)

if __name__ == '__main__':
    unittest.main()
