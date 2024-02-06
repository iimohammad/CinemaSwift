import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from db import models
from db.database_manager import DatabaseManager
import re
import uuid
import personalized_exceptions
import bcrypt
from datetime import datetime
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
    """

    """
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

# Users.AddUser(models.user_model(-1,'Masih32101','masih@abcd1.com','2000-01-01',None,3,'M@@@sih123'))
# print(Subscriptions.get_subscription_discount_value(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_subscription_discount_number(Subscriptions.get_subscription_type_name('d027e603-d459-4cf4-b533-c1c79f93fd52')))
# print(Subscriptions.get_total_discounts_taken('d027e603-d459-4cf4-b533-c1c79f93fd52'))
