import unittest
import re
from datetime import datetime
from  users import Subscriptions , UserInputValidator,Users

class SubscriptionsTest(unittest.TestCase):
    def add_subscription(self):
        user_id = "valid_user_id"  # Provide a valid user_id for testing
        subscription_id = 1
        result = Subscriptions.add_subscription(user_id, subscription_id)
        self.assertTrue(result)
        print("add_subscription test passed")

    def change_subscription(self):
        user_id = "valid_user_id"  # Provide a valid user_id for testing
        subscription_type_name = "valid_subscription_type"
        result = Subscriptions.change_subscription(user_id, subscription_type_name)
        self.assertTrue(result)
        print("change_subscription test passed")

    def get_subscription_type_name(self):
        user_id = "valid_user_id"
        result = Subscriptions.get_subscription_type_name(user_id)
        self.assertIsInstance(result, str)
        self.assertRegex(result, re.compile(r'^[a-zA-Z]+$'))
        print("get_subscription_type_name test passed")

    def get_subscription_discount_value(self):
        subscription_name = "valid_subscription_name"
        result = Subscriptions.get_subscription_discount_value(subscription_name)
        self.assertIsNotNone(result)
        print("get_subscription_discount_value test passed")

    def test_get_subscription_discount_number(self):
        subscription_name = "valid_subscription_name"
        result = Subscriptions.get_subscription_discount_number(subscription_name)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)
        print("get_subscription_discount_number test passed")

    def test_get_total_discounts_taken(self):
        user_id = "valid_user_id"
        result = Subscriptions.get_total_discounts_taken(user_id)
        self.assertIsInstance(result, int)
        print("get_total_discounts_taken test passed")

    def test_get_subscription_start_date(self):
        user_id = "valid_user_id"
        result = Subscriptions.get_subscription_start_date(user_id)
        self.assertIsInstance(result, datetime)
        print("get_subscription_start_date test passed")

    def test_buy_subscription(self):
        user_id = "valid_user_id"
        subs_type = "valid_subscription_type"
        # Assuming you have mocked the necessary dependencies to test this function
        result = Subscriptions.buy_subscription(user_id, subs_type)
        self.assertIsNone(result)
        print("buy_subscription test passed")

class UserInputValidator(Subscriptions):

    def _emailValidatorUser(self):
        # Valid phone number
        valid_phone = input("Enter a valid phone number: ")
        try:
            result = UserInputValidator._emailValidatorUser(valid_phone)
            print("Phone validation result:", result)
        except Exception as e:
            print("Phone validation error:", e)

    def hash_password(self):
        # Valid phone number
        Hashpassword = "valid_password"  # Provide a valid password for testing
        try:
            result = UserInputValidator._emailValidatorUser(Hashpassword)
            print("password is hash :", result)
        except Exception as e:
            print("Phone validation error:", e)

    def phone_validator(self):
        valid_phone = "09123456789"  # Provide a valid phone number for testing
        try:
            result = UserInputValidator.phone_validator(valid_phone)
            print("Phone validation result:", result)
        except Exception as e:
            print("Phone validation error:", e)
    
    def password_validator(self):
        valid_password = "Valid@Password1"  # Provide a valid password for testing
        try:
            result = UserInputValidator.password_validator(valid_password)
            print("Password validation result:", result)
        except Exception as e:
            print("Password validation error:", e)

    def username_validator(self):
        valid_username = "valid_username"  # Provide a valid username for testing
        try:
            result = UserInputValidator.username_validator(valid_username)
            print("Username validation result:", result)
        except Exception as e:
            print("Username validation error:", e)


class Users(UserInputValidator):

    def AddUser(self):
        user_data = models.user_model(
            username="john_doe",
            email="john@example.com",
            birthday="1990-01-01",
            phone="123456789",
            subscription_type_id="1",
            password="password123"
         )
        result = Users.AddUser(user_data)
        self.assertTrue(result)
        print("AddUser test passed.")

    def change_user_email(self):
        user_id = "valid_user_id"
        valid_email = "new_email@example.com"
        result = Users.change_user_email(user_id, valid_email)
        self.assertTrue(result)
        print("change_user_email test passed.")

    def change_user_phone(self):
        user_id = "valid_user_id"
        valid_phone = "987654321"
        result = Users.change_user_phone(user_id, valid_phone)
        self.assertTrue(result)
        print("change_user_phone test passed.")

    def _update_last_login(self):
        user_id = "valid_user_id"
        Users._update_last_login(user_id)
        print("_update_last_login test passed.")

    def username_validator_valid(self):
        valid_usernames = ['john_doe', 'alice123', 'user_name']
        for username in valid_usernames:
            with self.subTest(username=username):
                result = Users.username_validator(username)
                self.assertTrue(result)
                print(f"Username validation for {username}: Passed")

    def username_validator_invalid(self):
        invalid_usernames = ['user@name', 'user.name', 'user-name']
        for username in invalid_usernames:
            with self.subTest(username=username):
                result = Users.username_validator(username)
                self.assertFalse(result)
                print(f"Username validation for {username}: Passed")

if __name__ == '__main__':
    unittest.main()