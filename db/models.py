import datetime
from enum import Enum

# database
class UserType(Enum):
    USER = "User"
    MANAGER = "Manager"
    Admin = "Admin"
    
class SubscriptopnType(Enum):
    Golden = "Golden"
    Silver = "Silver"
    Bronze = "Bronze"
class person_model:
    def __init__(self,username:str,email:str,birthday:datetime,phone:str) -> None:
        self.username = username
        self.email = email
        self.birthday = birthday
        self.phone = phone
class bank_accounts_models:
    def __init__(self,id,user_id,balance,name,cvv2,password) -> None:
        self.id = id
        self.user_id = user_id
        self.balance = balance
        self.name = name
        self.cvv2 = cvv2
        self.password = password



class wallets_model:
    def __init__(self,id,balance,name,user_id) -> None:
        self.id = id
        self.balance = balance
        self.name = name
        self.user_id = user_id

class seats_showtimes_model:
    def __init__(self,id,sans_id,status) -> None:
        self.id = id
        self.sans_id = sans_id
        self.status = status

class sans_model:
    def __init__(self,id,screen_id,start_time,capacity) -> None:
        self.id = id
        self.screen_id = screen_id
        self.start_time = start_time
        self.capacity = capacity
class admin_model(person_model):
    def __init__(self,username:str,email:str,birthday:datetime,phone:str,user_type:UserType) -> None:
        super().__init__(username,email,birthday,phone)
        self.user_type = user_type


class users_model(person_model):
    def __init__(self,username:str,email:str,birthday:datetime,phone:str,suscription_type : SubscriptopnType) -> None:
        super().__init__(username,email,birthday,phone)
        self.user_type = UserType.USER
        self.suscription_type = suscription_type



class subscription_model:
    def __init__(self,id,name,descount_number,discount_value,drink_number) -> None:
        self.id = id
        self.name = name
        self.descount_number = descount_number
        self.discount_value = discount_value
        self.drink_number = drink_number
class comments_model:
    def __init__(self,id,film_id,user_id,text,date,parent_comments_id) -> None:
        self.id = id
        self.film_id = film_id
        self.user_id = user_id
        self.text = text
        self.date = date
        self.parent_comments_id = parent_comments_id

class free_drinks_model:
    def __init__(self,id,datetime) -> None:
        self.id = id
        self.datetime = datetime

class screens_mode:
    def __init__(self,id,film_id,number_of_screens) -> None:
        self.id = id
        self.film_id = film_id
        self.number_of_screens = number_of_screens

class films_model:
    def __init__(self,id,name,age_rating,duration,rate) -> None:
        self.id - id
        self.name = name
        self.age_rating = age_rating
        self.duration = duration
        self.rate = rate