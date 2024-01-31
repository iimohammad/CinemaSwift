from db import models
import re
import uuid

class BaseForUsersAndAdmins:
    @staticmethod
    def hashPassword(password: str):
        return hash(password)
    @staticmethod
    def emailValidator(email: str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        if match:
            return True
        return False

    @staticmethod
    def phoneValidator(phone: str):
        pattern = r'^09\d{9}$'
        match = re.match(pattern, phone)
        if match:
            return True
        return False
    @staticmethod
    def PasswordValidator(password:str):
        if len(password) < 8:
            return False
        if sum(1 for char in password if char in ['@', '#', '&', '$']) < 2:
            return False

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
            return False
        return True
    
    @staticmethod
    def UserNameValidator(username:str):
        if len(username)>100:
            return False
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', username):
            return True
        
        #also username should be uniqe
        
        return False
    @staticmethod
    def updateUserEmail(user_id:str,email:str):
        if Users.emailValidator(email):
            #update
            return True
        return False
    
class Users(BaseForUsersAndAdmins):
    
    @staticmethod
    def AddUser(user:models.users_model):
        if not Users.emailValidator(user.email):
            return False
        if user.phone !=None and not Users.phoneValidator(user.phone):
            return False
        
        user_id = uuid.uuid4()
        #also add to database
        
        return True
class Admins(BaseForUsersAndAdmins):
    @staticmethod
    def AddAdmin(user:models.users_model):
        if not Users.emailValidator(user.email):
            return False
        if user.phone !=None and not Users.phoneValidator(user.phone):
            return False
        
        user_id = uuid.uuid4()
        #also add to database
        return True
    