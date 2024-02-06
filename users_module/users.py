from db import models
from db.database_manager import DatabaseManager
import re
import uuid
from users_module import personalized_exceptions
import bcrypt
from datetime import datetime


class BaseForUsersAndAdmins:

    database_manager = DatabaseManager()

    @staticmethod
    def _hashPassword(password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def _phoneValidator(phone: str):
        pattern = r'^09\d{9}$'
        match = re.match(pattern, phone)
        if not match:
            raise personalized_exceptions.InvalidPhoneError()
        return True

    @staticmethod
    def PasswordValidator(password: str):
        if len(password) < 8:
            raise personalized_exceptions.ShortPasswordError(len(password), 8)
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            raise personalized_exceptions.NoSpecialCharacterError()

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise personalized_exceptions.ComplexityError()
        return True

    @staticmethod
    def _UserNameValidator(username: str):
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
    @staticmethod
    def _emailValidatorUser(email: str):
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
        query = f"""UPDATE users SET last_login = '{
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
        Users.database_manager.execute_query(query)

    @staticmethod
    def log_in(user_name: str, password: str):
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
    @staticmethod
    def _emailValidatorAdmin(email: str):
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