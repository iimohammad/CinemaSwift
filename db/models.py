import datetime
from enum import Enum


class UserType(Enum):
    USER = "User"
    MANAGER = "Manager"
    Admin = "Admin"


class person_model:
    def __init__(
            self,
            username: str,
            email: str,
            birthday: datetime,
            phone: str,
            register_date: datetime,
            last_login_date: datetime) -> None:
        self.username = username
        self.email = email
        self.birthday = birthday
        self.phone = phone
        self.register_date = register_date
        self.last_login_date = last_login_date


class user_Wallet_model:
    def __init__(
            self,
            bankAccount_name,
            bankAccount_cvv2,
            bankAccount_balance) -> None:
        self.bankAccount_name = bankAccount_name
        self.bankAccount_cvv2 = bankAccount_cvv2
        self.bankAccount_balance = bankAccount_balance


class cinema_model:
    def __init__(self, cinema_id, cinema_name) -> None:
        self.cinema_id = cinema_id
        self.cinema_name = cinema_name


class movie_showtimes_model:
    def __init__(self, showtime, movie_name, movie_id, num_show) -> None:
        self.mvoie_id = movie_id
        self.movie_name = movie_name
        self.showtime = showtime
        self.num_show = num_show


class chairs_showtimes_model:
    def __init__(self, user_id, chair_id) -> None:
        self.user_id = user_id
        self.chair_id = chair_id


class admin_model(person_model):
    def __init__(
            self,
            username: str,
            email: str,
            birthday: datetime,
            phone: str) -> None:
        super().__init__(username, email, birthday, phone)
        self.user_type = UserType.Admin


class users_model(person_model):
    def __init__(
            self,
            username: str,
            email: str,
            birthday: datetime,
            phone: str) -> None:
        super().__init__(username, email, birthday, phone)
        self.user_type = UserType.USER


class comments_model:
    def __init__(
            self,
            comment_id,
            movie_id,
            cinema_id,
            cinema_score,
            text_comment,
            ref_comment_id) -> None:
        self.comment_id = comment_id
        self.ref_comment_id = ref_comment_id
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.cinema_score = cinema_score
        self.text_comment = text_comment

        # when reply to a comment new comment ref to that
