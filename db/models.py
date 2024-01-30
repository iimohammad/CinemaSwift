

class person_model:
    def __init__(self,username) -> None:
        username = self.username
        subscription = None

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
    def __init__(self, username) -> None:
        super().__init__(username)


class users_model(person_model):
    def __init__(self, username) -> None:
        super().__init__(username)

class comments_model:
    def __init__(self) -> None:
        pass
