from re import Match
from db import models
import re
import uuid
from users_module import personalized_exceptions
import bcrypt
from users_module import queryset
from datetime import datetime


class UserInputValidator:
    """
    A class for validating user input data.
    This class provides static methods for validating various types of user input,
    including passwords, phone numbers, and usernames.

    Attributes:
        None
    """

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
        match: Match[str] | None = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        r = queryset.email_exist_check(email)
        if len(r) > 0:
            raise personalized_exceptions.InvalidEmailError()
        return True

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
        if Users.username_validator(user.username):
            if Users._emailValidatorUser(user.email):
                if user.phone is None or Users.phone_validator(user.phone):
                    user_id = str(uuid.uuid4())
                    user_data = {
                        'id': user_id,
                        'user_name': user.username,
                        'email': user.email,
                        'birthday': user.birthday,
                        'phone': user.phone,
                        'password': Users.hash_password(
                            user.password),
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'last_login': None,
                        'is_admin': 0
                    }

                    queryset.add_user_query(user_data)
        return True

    @staticmethod
    def update_user_email(user_id: str, email: str):
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
        if not Users._emailValidatorUser(email):
            raise personalized_exceptions.InvalidEmailError()
        queryset.update_user_email_query(user_id, email)

    @staticmethod
    def update_user_phone(user_id: str, phone: str):
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
        if not Users.phone_validator(phone):
            raise personalized_exceptions.InvalidPhoneError()
        queryset.update_user_phone_query(user_id, phone)

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
    def set_created_at(user_id):
        """
        this method use for set the time that user or admin was created the accounts
        """
        queryset.set_created_at(user_id=user_id)
