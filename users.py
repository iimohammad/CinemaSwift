from db import models
import re


class Users:
    def __init__(self):
        self.users = dict()
        self.admins = dict()

    @staticmethod
    def hashPassword(password: str):
        return hash(password)

    @staticmethod
    def updateUser(user: models.users_model):
        pass

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
