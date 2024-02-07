import datetime
from enum import Enum


# database


class AdminType(Enum):
    MANAGER = "Manager"
    Admin = "Admin"


class SubscriptopnType(Enum):
    Golden = "Golden"
    Silver = "Silver"
    Bronze = "Bronze"


class person_model:
    def __init__(
            self,
            id: str,
            username: str,
            email: str,
            birthday: datetime,
            phone: str,
            password: str) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.birthday = birthday
        self.phone = phone
        self.password = password


class admin_model(person_model):
    def __init__(
            self,
            id: str,
            username: str,
            email: str,
            birthday: datetime,
            phone: str,
            password: str,
            admin_type: AdminType) -> None:
        super().__init__(id, username, email, birthday, phone, password)
        self.admin_type = admin_type


class user_model(person_model):
    def __init__(
            self,
            id: str,
            username: str,
            email: str,
            birthday: datetime,
            phone: str,
            subscription_type_id: int,
            password: str,
            is_admin: int) -> None:
        super().__init__(id, username, email, birthday, phone, password)
        self.is_admin = is_admin
        self.subscription_type_id = subscription_type_id


class subscription_model:
    def __init__(
            self,
            id: int,
            name: str,
            discount_number: int,
            discount_value: int,
            drink_number: int) -> None:
        self.id = id
        self.name = name
        self.descount_number = discount_number
        self.discount_value = discount_value


class user_subscriptions_model:
    def __init__(
            self,
            user_id: str,
            subscription_id: int,
            start_date: str) -> None:
        self.user_id = user_id
        self.subscription_id = subscription_id
        self.start_date = start_date


class film_model:
    def __init__(
            self,
            id: int,
            name: str,
            age_rating: int,
            duration: int,
            point: int) -> None:
        self.id = id
        self.name = name
        self.age_rating = age_rating
        self.duration = duration
        self.point = point


class comment_model:
    def __init__(
            self,
            id: int,
            film_id: int,
            user_id: str,
            text: str,
            parent_comments_id: int,
            created_at: datetime) -> None:
        self.id = id
        self.film_id = film_id
        self.user_id = user_id
        self.text = text
        self.parent_comments_id = parent_comments_id
        self.created_at = created_at


class film_point_model:
    def __init__(self, film_id: int, user_id: str, point: int) -> None:
        self.film_id = film_id
        self.user_id = user_id
        self.point = point


class bank_account_model:
    def __init__(
            self,
            id: int,
            user_id: str,
            name: str,
            balance: int,
            cvv2: int,
            password: str) -> None:
        self.id = id
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.cvv2 = cvv2
        self.password = password


class wallet_model:
    def __init__(self, id: int, user_id: str, balance: int) -> None:
        self.id = id
        self.user_id = user_id
        self.balance = balance


class screen_model:
    def __init__(self, id: int, film_id: int, number_of_screens: int) -> None:
        self.id = id
        self.film_id = film_id
        self.number_of_screens = number_of_screens


class session_model:
    def __init__(
            self,
            id: int,
            screen_id: int,
            start_time: datetime,
            capacity: int,
            ticket_price: int) -> None:
        self.id = id
        self.screen_id = screen_id
        self.start_time = start_time
        self.capacity = capacity
        self.ticket_price = ticket_price


class seat_model:
    def __init__(self, id: int, session_id: int, status: str) -> None:
        self.id = id
        self.session_id = session_id
        self.status = status


class refun_droll_model:
    def __init__(self, id: int, name: str, percent_value: int):
        self.id = id
        self.name = name
        self.percent_value = percent_value
