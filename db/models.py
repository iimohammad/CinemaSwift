import datetime
from enum import Enum


class UserType(Enum):
    USER = "User"
    MANAGER = "Manager"
    Admin = "Admin"
class person_model:
    def __init__(self,username:str,email:str,birthday:datetime,phone:str) -> None:
        self.username = username
        self.email = email
        self.birthday = birthday
        self.phone = phone
class user_BankAccount_model:
    def __init__(self) -> None:
        pass



class user_Wallet_model:
    def __init__(self) -> None:
        pass


class movie_showtimes_model:
    def __init__(self) -> None:
        pass


class chairs_showtimes_model:
    def __init__(self) -> None:
        pass


class admin_model(person_model):
    def __init__(self,username:str,email:str,birthday:datetime,phone:str) -> None:
        super().__init__(username,email,birthday,phone)
        self.user_type = UserType.Admin


class users_model(person_model):
    def __init__(self,username:str,email:str,birthday:datetime,phone:str) -> None:
        super().__init__(username,email,birthday,phone)
        self.user_type = UserType.USER

class comments_model:
    def __init__(self) -> None:
        pass
