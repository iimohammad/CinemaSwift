from db import models
from db.database_manager import DatabaseManager
import re
import uuid
from users_module import personalized_exceptions
import bcrypt
from datetime import datetime


class BaseForUsersAndAdmins:
    """
    A base class providing common functionality for users and admins.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    database_manager = DatabaseManager()

    @staticmethod
    def _hashPassword(password: str):
        """
        Hashes the provided password using bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def _phoneValidator(phone: str):
        """
        Validates a phone number.

        Args:
            phone (str): The phone number to be validated.

        Returns:
            bool: True if the phone number is valid; otherwise, raises an exception.

        Raises:
            personalized_exceptions.InvalidPhoneError: If the phone number is invalid.
        """
        pattern = r'^09\d{9}$'
        match = re.match(pattern, phone)
        if not match:
            raise personalized_exceptions.InvalidPhoneError()
        return True

    @staticmethod
    def PasswordValidator(password: str):
        """
        Validates the complexity of a password.

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password is valid; otherwise, raises an exception.

        Raises:
            personalized_exceptions.ShortPasswordError: If the password is too short.
            personalized_exceptions.NoSpecialCharacterError: If the password lacks special characters.
            personalized_exceptions.ComplexityError: If the password complexity requirements are not met.
        """
        if len(password) < 8:
            raise personalized_exceptions.ShortPasswordError(len(password), 8)
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            raise personalized_exceptions.NoSpecialCharacterError()

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise personalized_exceptions.ComplexityError()
        return True

    @staticmethod
    def _UserNameValidator(username: str):
        """
        Validates a username.

        Args:
            username (str): The username to be validated.

        Returns:
            bool: True if the username is valid; otherwise, raises an exception.

        Raises:
            personalized_exceptions.LongUserNmaeError: If the username is too long.
            personalized_exceptions.UsernameTakenError: If the username is already taken.
            personalized_exceptions.ComplexityError: If the username complexity requirements are not met.
        """
        if len(username) > 100:
            raise personalized_exceptions.LongUserNmaeError(len(username), 100)
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', username):
            raise personalized_exceptions.ComplexityError()
        query = f"""
            SELECT user_name
            FROM users
            WHERE user_name = '{username}'
            UNION
            SELECT user_name
            FROM admins
            WHERE user_name = '{username}';
            """
        r = Users.database_manager.execute_query_select(query)
        if len(r) > 0:
            raise personalized_exceptions.UsernameTakenError()
        return True


class Users(BaseForUsersAndAdmins):
    """
    A class for managing user operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    @staticmethod
    def _emailValidatorUser(email: str):
        """
        Validates a user email.

        Args:
            email (str): The email to be validated.

        Returns:
            bool: True if the email is valid; otherwise, raises an exception.

        Raises:
            personalized_exceptions.InvalidEmailError: If the email is invalid or already exists.
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            SELECT email
            FROM users
            WHERE email = '{email}'
            """
        r = BaseForUsersAndAdmins.database_manager.execute_query_select(query)
        if len(r) > 0:
            raise personalized_exceptions.InvalidEmailError()
        return True

    @staticmethod
    def AddUser(user: models.user_model):
        """
        Adds a new user to the database.

        Args:
            user (models.user_model): The user model containing user information.

        Returns:
            bool: True if the user is successfully added; otherwise, False.
        """
        if Users._UserNameValidator(user.username):
            if Users._emailValidatorUser(user.email):
                if user.phone is None or Users._phoneValidator(user.phone):
                    user_id = str(uuid.uuid4())
                    user_data = {
                        'id': user_id,
                        'user_name': user.username,
                        'email': user.email,
                        'birthday': user.birthday,
                        'phone': user.phone,
                        'password': Users._hashPassword(
                            user.password)}

                    insert_query = """
                        INSERT INTO users
                        (id, user_name, email, birthday, phone,  password)
                        VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(password)s)
                    """
                    Users.database_manager.execute_query(
                        insert_query, user_data)
        return True

    @staticmethod
    def updateUserEmail(user_id: str, email: str):
        """
        Updates the email of a user in the database.

        Args:
            user_id (str): The ID of the user.
            email (str): The new email.

        Raises:
            personalized_exceptions.InvalidEmailError: If the email is invalid.
        """
        if not Users._emailValidatorUser(email):
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            UPDATE users
            SET email = '{email}'
            WHERE id = '{user_id}';
        """
        Users.database_manager.execute_query(query)

    @staticmethod
    def updateUserPhone(user_id: str, phone: str):
        """
        Updates the phone number of a user in the database.

        Args:
            user_id (str): The ID of the user.
            phone (str): The new phone number.

        Raises:
            personalized_exceptions.InvalidPhoneError: If the phone number is invalid.
        """
        if not Users._phoneValidator(phone):
            raise personalized_exceptions.InvalidPhoneError()
        query = f"""
            UPDATE users
            SET phone = '{phone}'
            WHERE id = '{user_id}';
        """
        Users.database_manager.execute_query(query)

    @staticmethod
    def _update_last_login(user_id: str):
        """
        Updates the last login timestamp of a user in the database.

        Args:
            user_id (str): The ID of the user.
        """
        query = f"""UPDATE users SET last_login = '{
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
        Users.database_manager.execute_query(query)

    @staticmethod
    def log_in(user_name: str, password: str):
        """
        Logs in a user with the provided credentials.

        Args:
            user_name (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: The ID of the logged-in user if successful; otherwise, False.
        """
        query = f"""
                    SELECT id,password FROM users
                    WHERE user_name = '{user_name}'
                """
        r = Users.database_manager.execute_query_select(query)
        if bcrypt.checkpw(password.encode('utf-8'), r[0][1].encode('utf-8')):
            user_id = r[0][0]
            Users._update_last_login(user_id)
            return user_id
        return False


class Admins(BaseForUsersAndAdmins):
    """
    A class for managing admin operations.

    Attributes:
        database_manager (DatabaseManager): Instance of the DatabaseManager class.
    """
    @staticmethod
    def _emailValidatorAdmin(email: str):
        """
        Validates an admin email.

        Args:
            email (str): The email to be validated.

        Returns:
            bool: True if the email is valid; otherwise, raises an exception.

        Raises:
            personalized_exceptions.InvalidEmailError: If the email is invalid or already exists.
        """
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            SELECT email
            FROM admins
            WHERE email = '{email}'
            """
        r = BaseForUsersAndAdmins.database_manager.execute_query_select(query)
        if len(r) > 0:
            raise personalized_exceptions.InvalidEmailError()
        return True

    @staticmethod
    def AddAdmin(user: models.admin_model):
        """
        Adds a new admin to the database.

        Args:
            user (models.admin_model): The admin model containing admin information.

        Returns:
            bool: True if the admin is successfully added; otherwise, False.
        """
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
        """
        Updates the username of an admin in the database.

        Args:
            user_id (str): The ID of the admin.
            user_name (str): The new username.

        Raises:
            personalized_exceptions.LongUserNmaeError: If the username is too long.
            personalized_exceptions.UsernameTakenError: If the username is already taken.
            personalized_exceptions.ComplexityError: If the username complexity requirements are not met.
        """
        if Admins._UserNameValidator(user_name):
            query = f"""
            UPDATE admins
            SET user_name = '{user_name}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def updateAdminEmail(user_id: str, email: str):
        """
        Updates the email of an admin in the database.

        Args:
            user_id (str): The ID of the admin.
            email (str): The new email.

        Raises:
            personalized_exceptions.InvalidEmailError: If the email is invalid.
        """
        if Admins._emailValidatorAdmin(email):
            query = f"""
            UPDATE admins
            SET email = '{email}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def updateAdminPhone(user_id: str, phone: str):
        """
        Updates the phone number of an admin in the database.

        Args:
            user_id (str): The ID of the admin.
            phone (str): The new phone number.

        Raises:
            personalized_exceptions.InvalidPhoneError: If the phone number is invalid.
        """
        if Admins._phoneValidator(phone):
            query = f"""
            UPDATE admins
            SET phone = '{phone}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)

    @staticmethod
    def _update_last_login(user_id: str):
        """
        Updates the last login timestamp of an admin in the database.

        Args:
            user_id (str): The ID of the admin.
        """
        query = f"""UPDATE admins SET last_login = '{
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
        Admins.database_manager.execute_query(query)

    @staticmethod
    def log_in(user_name: str, password: str):
        """
        Logs in an admin with the provided credentials.

        Args:
            user_name (str): The username of the admin.
            password (str): The password of the admin.

        Returns:
            str: The ID of the logged-in admin if successful; otherwise, False.
        """
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
