<<<<<<< HEAD
from re import Match
=======
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
>>>>>>> main
from db import models
import re
import uuid
import personalized_exceptions
import bcrypt
from users_module import queryset
from datetime import datetime
<<<<<<< HEAD


class UserInputValidator:
=======
class Subscriptions:
    database_manager = DatabaseManager()
    @staticmethod
    def add_subscription(user_id:str,subscription_id:int):
        query = f"""INSERT INTO `cinemaswift`.`userssubscriptions` (`user_id`, `subscription_id`, `start_date`) 
                VALUES 
                ('{user_id}', '{subscription_id}', '{datetime.now()}');"""
        Subscriptions.database_manager.execute_query(query)
        return True
        
    @staticmethod
    def change_subscription(user_id:str,subscription_type_name:str)->bool:
        query = f"""SELECT id FROM cinemaswift.subscriptions
                WHERE name = '{subscription_type_name}';"""
        r = Subscriptions.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.SubscriptionNotFount()
        
        query = f"""UPDATE `cinemaswift`.`users` SET `subscription_type_id` = '{r[0][0]}' 
                WHERE (`id` = '{user_id}');"""
        Subscriptions.database_manager.execute_query(query)
        return True
    @staticmethod
    def get_subscription_type_name(user_id:str)->str:
        query = f"""SELECT name FROM subscriptions
                where
                id = (SELECT subscription_type_id FROM cinemaswift.users where id = '{user_id}');"""
        return Subscriptions.database_manager.execute_query_select(query)[0][0]
    @staticmethod
    def get_subscription_discount_value(subscription_name:str):
        query = f"""SELECT discount_value FROM cinemaswift.subscriptions
                WHERE
                name = '{subscription_name}';"""
        
        return Subscriptions.database_manager.execute_query_select(query)[0][0]
    @staticmethod
    def get_subscription_discount_number(subscription_name:str):
        query = f"""SELECT discount_number FROM cinemaswift.subscriptions
                WHERE
                name = '{subscription_name}';"""
        return Subscriptions.database_manager.execute_query_select(query)[0][0]
    @staticmethod
    def get_total_discounts_taken(user_id:str)->int:
        query = f"""SELECT count(id) FROM cinemaswift.tickets
                WHERE created_at >= 
	                (select start_date FROM userssubscriptions WHERE user_id = '{user_id}');"""
        return Subscriptions.database_manager.execute_query_select(query)[0][0]
    @staticmethod
    def get_subscription_start_date(user_id:str)->datetime:
        query = f"""SELECT start_date FROM cinemaswift.userssubscriptions
        WHERE user_id = '{user_id}';"""
        return Subscriptions.database_manager.execute_query_select(query)[0][0]
        
class BaseForUsersAndAdmins:
>>>>>>> main
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
<<<<<<< HEAD
                        'password': Users.hash_password(
                            user.password),
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'last_login': None,
                        'is_admin': 0
                    }

                    queryset.add_user_query(user_data)
=======
                        'subscription_type_id' : user.subscription_type_id,
                        'password': Users._hashPassword(
                            user.password)}

                    insert_query = """
                        INSERT INTO users
                        (id, user_name, email, birthday, phone, subscription_type_id, password)
                        VALUES 
                        (%(id)s, %(user_name)s, %(email)s, %(birthday)s ,%(phone)s,%(subscription_type_id)s, %(password)s)
                    """
                    Users.database_manager.execute_query(
                        insert_query, user_data)
                    Subscriptions.add_subscription(user_id,3)
>>>>>>> main
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
<<<<<<< HEAD
    def set_created_at(user_id):
        """
        this method use for set the time that user or admin was created the accounts
        """
        queryset.set_created_at(user_id=user_id)
=======
    def AddAdmin(user: models.admin_model):
        if Admins._UserNameValidator(user.username):
            if Admins._emailValidatorAdmin(user.email):
                if user.phone is None or Admins._phoneValidator(user.phone):
                    user_id = str(uuid.uuid4())
                    user_data = {
                        'id': user_id,
                        'user_name': user.username,
                        'email': user.email,
                        'birthday': user.birthday,
                        'phone': user.phone,
                        'admin_type': user.admin_type,
                        'password': Admins._hashPassword(
                            user.password)}

                    insert_query = """
                        INSERT INTO admins
                        (id, user_name, email, birthday, phone, admin_type, password)
                        VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(admin_type)s, %(password)s)
                    """
                    Admins.database_manager.execute_query(
                        insert_query, user_data)
        return True

    @staticmethod
    def updateAdminUserName(user_id: str, user_name: str):
        if Admins._UserNameValidator(user_name):
            query = f"""
            UPDATE admins
            SET user_name = '{user_name}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def updateAdminEmail(user_id: str, email: str):
        if Admins._emailValidatorAdmin(email):
            query = f"""
            UPDATE admins
            SET email = '{email}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def updateAdminPhone(user_id: str, phone: str):
        if Admins._phoneValidator(phone):
            query = f"""
            UPDATE admins
            SET phone = '{phone}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def _update_last_login(user_id: str):
        query = f"""UPDATE admins SET last_login = '{
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
        Admins.database_manager.execute_query(query)

    @staticmethod
    def log_in(user_name: str, password: str):
        query = f"""
                    SELECT id,password FROM cinemaswift.admins
                    WHERE user_name = '{user_name}'
                """
        r = Admins.database_manager.execute_query_select(query)
        if bcrypt.checkpw(password.encode('utf-8'), r[0][1].encode('utf-8')):
            user_id = r[0][0]
            Admins._update_last_login(user_id)
            return user_id
        return False

# Users.AddUser(models.user_model(-1,'Masih32101','masih@abcd1.com','2000-01-01',None,3,'M@@@sih123'))
# print(Subscriptions.get_subscription_discount_value(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_subscription_discount_number(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_total_discounts_taken('d027e603-d459-4cf4-b533-c1c79f93fd52'))
>>>>>>> main
