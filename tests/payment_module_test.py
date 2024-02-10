import unittest
from unittest.mock import MagicMock, patch
from payment_module import bankaccounts, queryset
from users_module import personalized_exceptions
from datetime import datetime
import os

class TestBankAccounts(unittest.TestCase):

    def setUpClass(cls):
        #comming soon
        pass

    def test_hashPassword(self):
        password = "12345jlk"
        hashed_password = bankaccounts._hashPassword(password)
        self.assertTrue(hashed_password) 

    def test_cvv2_validator_valid(self):
        cvv = 123
        self.assertIsNone(bankaccounts.cvv2_validator(cvv))  

    def test_cvv2_validator_invalid(self):
        cvv = 12345
        with self.assertRaises(personalized_exceptions.InvalidCvv2):
            bankaccounts.cvv2_validator(cvv)  

    def test_add_log(self):
        log_text = "Test log entry"
        bankaccounts.add_log(log_text)
        with open(self.log_file, 'a') as f:
            f.write(
                log_text +
                f""" _ at {
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""" +
                os.linesep)
            log_text = "Test log entry"
        with open(bankaccounts.log_file, 'r') as f:
            lines = f.readlines()
            self.assertTrue(any(log_text in line for line in lines))  

    def test_add_bank_account_success(self):
        mock_bank_account = MagicMock()
        mock_bank_account.user_id = "22"
        mock_bank_account.name = "peyman"
        mock_bank_account.balance = 1000
        mock_bank_account.cvv2 = 123
        mock_bank_account.password = "ali02012001"
        queryset.check_bank_account_query.return_value = [(0,)]  
        result = bankaccounts.add_bank_account(mock_bank_account)
        self.assertTrue(result)  


    def test_get_bank_accounts(self):
        user_id = "123"
        queryset.get_bank_accounts_query.return_value = [("Test Account",), ("Another Account",)]  
        result = bankaccounts.get_bank_accounts(user_id)
        self.assertEqual(len(result), 2) 

    def test_get_bank_account_balance_valid(self):
        user_id = "123"
        account_name = "Test Account"
        cvv = 123
        password = "password123"
        queryset.get_bank_accounts_balance_query.return_value = [(cvv, password, 1000)]  
        result = bankaccounts.get_bank_account_balance(user_id, account_name, cvv, password)
        self.assertEqual(result, "Test Account : 1000")  

    def test_deposit_to_bank_account(self):
        user_id = "123"
        account_name = "Test Account"
        amount = 500
        queryset.deposit_to_bank_account_query.return_value = [(1, 1000)] 
        result = bankaccounts.deposit_to_bank_account(user_id, account_name, amount)
        self.assertTrue(result) 

    def test_harvest_from_bank_account(self):
        user_id = "123"
        cvv = 123
        password = "password123"
        amount = 500
        account_name = "Test Account"
        queryset.harvest_from_account.return_value = [(1, "Test Account", 1000, 123, "password123", 500)]  # حساب موجود و با موجودی و کلمه عبور و سی‌وی‌وی درست
        result = bankaccounts.harvest_from_bank_account(user_id, cvv, password, amount, account_name)
        self.assertTrue(result) 

    def test_money_transfer(self):
        user_id_origin = "123"
        account_name_origin = "Origin Account"
        cvv = 123
        password = "password123"
        user_id_destination = "456"
        account_name_destination = "Destination Account"
        amount = 500
        queryset.get_bank_accounts_balance_query.return_value = [(cvv, password, 1000)]  
        queryset.deposit_to_bank_account_query.return_value = [(1, 500)]  
        result = bankaccounts.money_transfer(user_id_origin, account_name_origin, cvv, password, user_id_destination, account_name_destination, amount)
        self.assertTrue(result)  

if __name__ == '__main__':
    unittest.main()

