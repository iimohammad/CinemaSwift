import unittest
import re
from datetime import datetime
from  users_module import Subscriptions , UserInputValidator,Users

class Subscriptions(unittest.TestCase):
    def add_subscription(self):
        user_id = input("")
        subscription_id = 1
        result = Subscriptions.add_subscription(user_id, subscription_id)
        self.assertTrue(result)
        print("add_subscription test passed")

    def change_subscription(self):
        user_id = input("")
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

    def test_get_subscription_discount_value(self):
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
        Hashpassword = input("Enter a valid password: ")
        try:
            result = UserInputValidator._emailValidatorUser(Hashpassword)
            print("password is hash :", result)
        except Exception as e:
            print("Phone validation error:", e)

    def phone_validator(self):
        # Valid phone number
        valid_phone = input("Enter a valid phone number: ")
        try:
            result = UserInputValidator._phone_validator(valid_phone)
            print("Phone validation result:", result)
        except Exception as e:
            print("Phone validation error:", e)

    
    def password_validator(self):
        # Valid phone number
        password = input("Enter a valid password: ")
        try:
            result = UserInputValidator.password_validator(password)
            print("password is hash :", result)
        except Exception as e:
            print("Phone validation error:", e)

    def username_validator(self):
        # Valid phone number
        username_validator = input("Enter a username_validator: ")
        try:
            result = UserInputValidator.username_validator(username_validator)
            print("Phone validation result:", result)
        except Exception as e:
            print("Phone validation error:", e)


class Users(UserInputValidator):

    def AddUser(self):
        user_data = models.user_model(
            username=input(""),
            email=input(""),
            birthday=input(""),
            phone=input(""),
            subscription_type_id=input(""),
            password=input("")
        )
        result = Users.AddUser(user_data)
        self.assertTrue(result)
        print("AddUser test passed.")

    def change_user_email(self):
        user_id = input("")
        valid_email = input("")
        result = Users.change_user_email(user_id, valid_email)
        self.assertTrue(result)
        print("change_user_email test passed.")

    def change_user_phone(self):
        user_id = input("")
        valid_phone = input("")
        result = Users.change_user_email(user_id, valid_phone)
        self.assertTrue(result)
        print("change_user_phone test passed.")

    def _update_last_login(self):
        user_id = input("")
        Users._update_last_login(user_id)
        print("_update_last_login test passed.")

    def test_username_validator_valid(self):
        valid_usernames = ['john_doe', 'alice123', 'user_name']
        for username in valid_usernames:
            with self.subTest(username=username):
                result = Users.username_validator(username)
                self.assertTrue(result)
                print(f"Username validation for {username}: Passed")

    def test_username_validator_invalid(self):
        invalid_usernames = ['user@name', 'user.name', 'user-name']
        for username in invalid_usernames:
            with self.subTest(username=username):
                result = Users.username_validator(username)
                self.assertFalse(result)
                print(f"Username validation for {username}: Passed")

    def log_in(self):
        user_name = input("")
        password = input("")

        # Mocking the queryset result
        queryset.login_query = lambda x: [("valid_user_id", bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))]

        result = Users.log_in(user_name, password)
        self.assertEqual(result, "valid_user_id")
        print("log_in test passed.")

if __name__ == '__main__':
    unittest.main()