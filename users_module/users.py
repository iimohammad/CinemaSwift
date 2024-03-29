from db import models
import re
import uuid
from users_module import personalized_exceptions
import bcrypt
from users_module import queryset
from datetime import date, datetime
from payment_module.wallet import Wallets


class Subscriptions:
    @staticmethod
    def add_subscription(user_id: str, subscription_id: int):
        queryset.add_subscription_query(user_id, subscription_id)
        return True

    @staticmethod
    def change_subscription(user_id: str, subscription_type_name: str) -> bool:
        queryset.change_subscription_query(user_id, subscription_type_name)
        return True

    @staticmethod
    def get_subscription_type_name(user_id: str) -> str:
        result = queryset.get_subscription_type_name_query(user_id=user_id)
        return result[0][0]

    @staticmethod
    def get_subscription_discount_value(user_id: str):
        result = queryset.get_subscription_discount_value_query(user_id)
        return result[0][0]

    @staticmethod
    def get_subscription_discount_number(subscription_name: str):
        result = queryset.get_subscription_discount_number_query(subscription_name)
        return result

    @staticmethod
    def get_total_discounts_taken(user_id: str) -> int:
        result = queryset.get_total_discounts_taken_query(user_id=user_id)
        return result

    @staticmethod
    def get_subscription_start_date(user_id: str) -> datetime:
        result = queryset.get_subscription_start_date_query(user_id=user_id)
        return result

    @staticmethod
    def buy_subscription(user_id, subs_type):
        #buy desire subs and decrease from wallet, if wallet does not have enough balace wants to charge it
        pass

class UserInputValidator:
    """
    A class for validating user input data.
    This class provides static methods for validating various types of user input,
    including passwords, phone numbers, and usernames.

    Attributes:
        None
    """
    @staticmethod
    def _emailValidatorUser(email: str):
        """
                Validates an email address for a user.

                Args:
                    email (str): The email address to be validated.

                Returns:
                    bool: True if the email address is valid.

                Raises:
                    personalized_exceptions.InvalidEmailError: If the email address is invalid or already exists.
        """
        pattern: str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match: re.Match[str] | None = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        r = queryset.email_exist_check_query(email)
        if len(r) > 0:
            raise personalized_exceptions.InvalidEmailError()
        return True
    @staticmethod
    def hash_password(password: str) -> object:
        """
                Hashes the provided password using bcrypt.

                Args:
                    password (str): The password to be hashed.

                Returns:
                    object: A hashed representation of the password.

                Raises:
                    None
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def phone_validator(phone: str):
        """
                Validates a phone number.

                Args:
                    phone (str): The phone number to be validated.

                Returns:
                    bool: True if the phone number is valid.

                Raises:
                    personalized_exceptions.InvalidPhoneError: If the phone number does not match the required pattern.
        """
        pattern = r'^09\d{9}$'
        match = re.match(pattern, phone)
        if not match:
            raise personalized_exceptions.InvalidPhoneError()
        return True

    @staticmethod
    def password_validator(password: str):
        """
                Validates a password.

                Args:
                    password (str): The password to be validated.

                Returns:
                    bool: True if the password is valid.

                Raises:
                    personalized_exceptions.ShortPasswordError: If the password is too short.
                    personalized_exceptions.NoSpecialCharacterError: If the password does not contain enough special characters.
                    personalized_exceptions.ComplexityError: If the password does not meet complexity requirements.
        """
        if len(password) < 8:
            raise personalized_exceptions.ShortPasswordError(len(password), 8)
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            raise personalized_exceptions.NoSpecialCharacterError()

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise personalized_exceptions.ComplexityError()
        return True

    @staticmethod
    def username_validator(username: str):
        """
                Validates a username.

                Args:
                    username (str): The username to be validated.

                Returns:
                    bool: True if the username is valid.

                Raises:
                    personalized_exceptions.LongUsernameError: If the username is too long.
                    personalized_exceptions.ComplexityError: If the username does not meet complexity requirements.
                    personalized_exceptions.UsernameTakenError: If the username is already taken.
        """
        if len(username) > 100:
            raise personalized_exceptions.LongUserNmaeError(len(username), 100)
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', username):
            raise personalized_exceptions.ComplexityError()

        r = queryset.username_exits_check(username)
        if len(r) > 0:
            raise personalized_exceptions.UsernameTakenError()
        return True


class Users(UserInputValidator):
    """
        A class for managing user-related operations such as adding users, updating user information,
        logging in, and checking user roles.

        This class extends the UserInputValidator for validating user input data.

        Attributes:
            None
    """
    @staticmethod
    def calculateAge(birthDate):
        today = date.today()
        age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
        return age
    @staticmethod
    def get_user_id_by_username(username:str):
        return queryset.get_user_id_by_username_query(username)
    @staticmethod
    def AddUser(user: models.user_model):
        """
                Adds a new user to the system.
                Args:
                    user (models.user_model): An instance of the User model containing user information.
                Returns:
                    bool: True if the user is successfully added.
                Raises:
                    personalized_exceptions.InvalidUsernameError: If the username is invalid or already taken.
                    personalized_exceptions.InvalidEmailError: If the email address is invalid or already exists.
                    personalized_exceptions.InvalidPhoneError: If the phone number is invalid.
        """
        Users.username_validator(user.username)
        Users._emailValidatorUser(user.email)
        if user.phone is None or Users.phone_validator(user.phone):
            user_id = str(uuid.uuid4())
            user_data = {
                'id': user_id,
                'user_name': user.username,
                'email': user.email,
                'birthday': user.birthday,
                'phone': user.phone,
                'subscription_type_id': user.subscription_type_id,
                'password': Users.hash_password(user.password),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'last_login': None,
                'is_admin': user.is_admin
                }

            queryset.add_user_query(user_data)
            Wallets.create_wallet(user_id)
        return True

    @staticmethod
    def change_user_email(user_id: str, email: str)->bool:
        """
                Updates the email address of a user.

                Args:
                    user_id (str): The ID of the user whose email is to be updated.
                    email (str): The new email address.

                Returns:
                    None

                Raises:
                    personalized_exceptions.InvalidEmailError: If the email address is invalid.
        """
        Users._emailValidatorUser(email)
        queryset.update_user_email_query(user_id, email)
        return True
    @staticmethod
    def change_user_phone(user_id: str, phone: str)->bool:
        """
                Updates the phone number of a user.

                Args:
                    user_id (str): The ID of the user whose phone number is to be updated.
                    phone (str): The new phone number.

                Returns:
                    None

                Raises:
                    personalized_exceptions.InvalidPhoneError: If the phone number is invalid.
        """
        Users.phone_validator(phone)
        queryset.update_user_phone_query(user_id, phone)
        return True
    
    @staticmethod
    def _update_last_login(user_id: str):
        """
                Updates the last login time of a user.

                Args:
                    user_id (str): The ID of the user.

                Returns:
                    None
        """
        queryset.update_last_login_query(user_id)

    @staticmethod
    def log_in(user_name: str, password: str):
        """
                Logs in a user with the provided credentials.

                Args:
                    user_name (str): The username of the user.
                    password (str): The password of the user.

                Returns:
                    str: The ID of the user if login is successful, otherwise False.
        """
        r = queryset.login_query(user_name)
        if bcrypt.checkpw(password.encode('utf-8'), r[0][1].encode('utf-8')):
            user_id = r[0][0]
            Users._update_last_login(user_id)
            return user_id
        return False

    @staticmethod
    def set_admin(user_id):
        """
                Checks if a user is an admin.
                Args:
                    user_id: The ID of the user.
                Returns:
                    None
        """
        queryset.set_user_as_admin(user_id=user_id)

    @staticmethod
    def set_admin_by_username(username):
        """
                Checks if a user is an admin.

                Args:
                    username: The ID of the user.

                Returns:
                    None
        """
        queryset.set_user_as_admin_by_username(username=username)

    @staticmethod
    def get_user_birthday(user_id):
        return queryset.get_user_birthday_query(user_id)

    @staticmethod
    def is_admin(user_id:str):
        return queryset.is_admin_check_query(user_id)

    @staticmethod
    def change_username(user_id:str, new_username:str)->bool:
        Users.username_validator(new_username)
        queryset.change_username_query(user_id,new_username)
        return True

    @staticmethod
    def change_password(user_id:str, password:str)->bool:
        Users.password_validator(password)
        queryset.change_password_query(user_id , Users.hash_password(password))
        return True
    @staticmethod
    def show_profile(user_id:str)->dict:
        return queryset.show_profile_query(user_id)

    @staticmethod
    def remove_account(user_id):
        pass

# Users.AddUser(models.user_model(-1,'Masih321011','masih@abcd11.com','2000-01-01',None,3,'M@@@sih123',0))
# print(Subscriptions.get_subscription_discount_value(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_subscription_discount_number(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_total_discounts_taken('d027e603-d459-4cf4-b533-c1c79f93fd52'))
# print(Users.change_username('be3cf15b-e11b-4e62-9bbf-79b330700f09','Masih1999'))