from db import models
from db.database_manager import DatabaseManager
import re
import uuid
import personalized_exceptions


class BaseForUsersAndAdmins:
    
    database_manager = DatabaseManager('127.0.0.1','root',"M@sih2012",'cinemaswift')
    
    @staticmethod
    def hashPassword(password: str):
        return hash(password)

    @staticmethod
    def phoneValidator(phone: str):
        pattern = r'^09\d{9}$'
        match = re.match(pattern, phone)
        if not match:
            raise personalized_exceptions.InvalidPhoneError()
        return True
    
    @staticmethod
    def PasswordValidator(password:str):
        if len(password) < 8:
            raise personalized_exceptions.ShortPasswordError(len(password),8)
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            raise personalized_exceptions.NoSpecialCharacterError()

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            raise personalized_exceptions.ComplexityError()
        return True
    
    @staticmethod
    def UserNameValidator(username:str):
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
        r = BaseForUsersAndAdmins.database_manager.execute_query(query)
        if len(r)>0:
            raise personalized_exceptions.UsernameTakenError()
        return True
        
    
class Users(BaseForUsersAndAdmins):
    @staticmethod
    def emailValidatorUser(email: str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            SELECT email
            FROM users
            WHERE email = '{email}'
            """
        r = BaseForUsersAndAdmins.database_manager.execute_query(query)
        if len(r)!=0:
            raise personalized_exceptions.InvalidEmailError()
        return True
    @staticmethod
    def AddUser(user:models.user_model):
        if Users.UserNameValidator(user.username):
            if Users.emailValidatorUser(user.email):
                if user.phone ==None or Users.phoneValidator(user.phone):
                    user_id = str(uuid.uuid4())
                    print(user_id)
                    user_data = {'id': user_id,
                            'user_name': user.username,
                            'email': user.email,
                            'birthday': user.birthday,
                            'phone': user.phone,
                            'subscription_type': user.suscription_type,
                            'password': Users.hashPassword(user.password)}

                    insert_query = """
                        INSERT INTO users
                        (id, user_name, email, birthday, phone, subscription_type, password)
                        VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(subscription_type)s, %(password)s)
                    """
                    Users.database_manager.execute_query(insert_query,user_data)
        return True
    
    @staticmethod
    def updateUserEmail(user_id:str,email:str):
        if Users.emailValidatorUser(email):
            query = f"""
            SELECT email
            FROM users
            WHERE email = '{email}'
            """
class Admins(BaseForUsersAndAdmins):
    @staticmethod
    def emailValidatorAdmin(email: str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        if not match:
            raise personalized_exceptions.InvalidEmailError()
        query = f"""
            SELECT email
            FROM admins
            WHERE email = '{email}'
            """
        r = BaseForUsersAndAdmins.database_manager.execute_query(query)
        if len(r)!=0:
            raise personalized_exceptions.InvalidEmailError()
        return True
    @staticmethod
    def AddAdmin(user:models.user_model):
        if not Admins.emailValidatorAdmin(user.email):
            return False
        if user.phone !=None and not Users.phoneValidator(user.phone):
            return False
        
        user_id = uuid.uuid4()
        #also add to database
        return True
    @staticmethod
    def updateAdminEmail(user_id:str,email:str):
        if Admins.emailValidatorAdmin(email):
            query = f"""
            SELECT email
            FROM admins
            WHERE email = '{email}';
            """
            BaseForUsersAndAdmins.database_manager.connect()
            r = BaseForUsersAndAdmins.database_manager.execute_query(query)
            BaseForUsersAndAdmins.database_manager.disconnect()
            if len(r)==0:
                query = f"""
                SELECT email
                FROM users
                WHERE email = '{email}'
                """


Users.AddUser(models.user_model(-1,'Masih1','masih@abc.com','1999-12-12','09131231234','M@@@sih123',models.SubscriptopnType.Bronze.value))