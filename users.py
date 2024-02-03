from db import models
from db.database_manager import DatabaseManager
import re
import uuid
import personalized_exceptions
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
    def _PasswordValidator(password:str):
        if len(password) < 8:
            raise personalized_exceptions.ShortPasswordError(len(password),8)
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            raise personalized_exceptions.NoSpecialCharacterError()

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise personalized_exceptions.ComplexityError()
        return True
    
    @staticmethod
    def _UserNameValidator(username:str):
        if len(username)>100:
            raise personalized_exceptions.LongUserNmaeError(len(username),100)
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
        if len(r)>0:
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
        if len(r)>0:
            raise personalized_exceptions.InvalidEmailError()
        return True
    @staticmethod
    def AddUser(user:models.user_model):
        if Users._UserNameValidator(user.username):
            if Users._emailValidatorUser(user.email):
                if user.phone ==None or Users._phoneValidator(user.phone):
                    user_id = str(uuid.uuid4())
                    user_data = {'id': user_id,
                            'user_name': user.username,
                            'email': user.email,
                            'birthday': user.birthday,
                            'phone': user.phone,
                            'subscription_type': user.suscription_type,
                            'password': Users._hashPassword(user.password)}

                    insert_query = """
                        INSERT INTO users
                        (id, user_name, email, birthday, phone, subscription_type, password)
                        VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(subscription_type)s, %(password)s)
                    """
                    Users.database_manager.execute_query(insert_query,user_data)
        return True
    
    @staticmethod
    def updateUserEmail(user_id:str,email:str):
        if not Users._emailValidatorUser(email):
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            UPDATE users
            SET email = '{email}'
            WHERE id = '{user_id}';
        """
        Users.database_manager.execute_query(query)
    
    @staticmethod
    def updateUserPhone(user_id:str,phone:str):
        if not Users._phoneValidator(phone):
            raise personalized_exceptions.InvalidPhoneError()
        query = f"""
            UPDATE users
            SET phone = '{phone}'
            WHERE id = '{user_id}';
        """
        Users.database_manager.execute_query(query)
    @staticmethod
    def _update_last_login(user_id:str):
        query = f"UPDATE users SET last_login = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"
        Users.database_manager.execute_query(query)
    @staticmethod
    def log_in(user_name:str,password:str):
        query = f"""
                    SELECT id,password FROM cinemaswift.users
                    WHERE user_name = '{user_name}'
                """
        r = Users.database_manager.execute_query_select(query)
        if bcrypt.checkpw(password.encode('utf-8'),r[0][1].encode('utf-8')):
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
        if len(r)>0:
            raise personalized_exceptions.InvalidEmailError()
        return True
    @staticmethod
    def AddAdmin(user:models.admin_model):
        if Admins._UserNameValidator(user.username):
            if Admins._emailValidatorAdmin(user.email):
                if user.phone ==None or Admins._phoneValidator(user.phone):
                    user_id = str(uuid.uuid4())
                    user_data = {'id': user_id,
                            'user_name': user.username,
                            'email': user.email,
                            'birthday': user.birthday,
                            'phone': user.phone,
                            'admin_type': user.admin_type,
                            'password': Admins._hashPassword(user.password)}

                    insert_query = """
                        INSERT INTO admins
                        (id, user_name, email, birthday, phone, admin_type, password)
                        VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(admin_type)s, %(password)s)
                    """
                    Admins.database_manager.execute_query(insert_query,user_data)
        return True
    @staticmethod
    def updateAdminUserName(user_id:str,user_name:str):
        if Admins._UserNameValidator(user_name):
            query = f"""
            UPDATE admins
            SET user_name = '{user_name}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)
    @staticmethod
    def updateAdminEmail(user_id:str,email:str):
        if Admins._emailValidatorAdmin(email):
            query = f"""
            UPDATE admins
            SET email = '{email}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)
    @staticmethod
    def updateAdminPhone(user_id:str,phone:str):
        if Admins._phoneValidator(phone):
            query = f"""
            UPDATE admins
            SET phone = '{phone}'
            WHERE id = '{user_id}';
            """
        Users.database_manager.execute_query(query)
    
    @staticmethod
    def _update_last_login(user_id:str):
        query = f"UPDATE admins SET last_login = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"
        Admins.database_manager.execute_query(query)
    @staticmethod
    def log_in(user_name:str,password:str):
        query = f"""
                    SELECT id,password FROM cinemaswift.admins
                    WHERE user_name = '{user_name}'
                """
        r = Admins.database_manager.execute_query_select(query)
        if bcrypt.checkpw(password.encode('utf-8'),r[0][1].encode('utf-8')):
            user_id = r[0][0]
            Admins._update_last_login(user_id)
            return user_id
        return False

# Users.AddUser(models.user_model(-1,'Masih11','masih12@abc.com','1999-12-12','09131231234','M@@@sih123',models.SubscriptopnType.Bronze.value))
# r = Users.database_manager.execute_query_select("SELECT user_name FROM users WHERE user_name = 'Masih1' UNION SELECT user_name FROM admins WHERE user_name = 'Masih1';")
# print(r)
# Users.updateUserEmail('7a91adf0-bcb9-4e29-bba1-171e310aa30e','masih1234@abc.com')
# Admins.AddAdmin(models.admin_model(-1,'Ali1','masih1211@abc.com','1999-12-12','09131231234','M@@@sih123',models.AdminType.MANAGER.value))
# Admins.updateAdminEmail('df3cf799-ca17-41e2-a566-9bac7a67f633','masih123@abc.com')
# Admins.log_in('Ali1','M@@@sih123')
# print(Users.log_in('Masih11','M@@@sih1233'))
# Admins.updateAdminUserName('df3cf799-ca17-41e2-a566-9bac7a67f633','Masih111')
