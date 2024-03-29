class ShortPasswordError(Exception):
    def __init__(self, password_length, minimum_length):
        super().__init__(f"""Password must be at least {
            minimum_length} characters long, but got {password_length} characters.""")


class NoSpecialCharacterError(Exception):
    def __init__(self):
        super().__init__("Password must contain at least three special character (# , @ , & , &).")


class ComplexityError(Exception):
    def __init__(self):
        super().__init__("Must contain Uppercase and lowercase letters and numbers.")


class LongUserNmaeError(Exception):
    def __init__(self, user_name_length, maximum_length):
        super().__init__(f"""User name must be less or equal {
            maximum_length} characters long, but got {user_name_length} characters.""")


class InvalidEmailError(Exception):
    def __init__(self):
        super().__init__("Invalid email address.")


class InvalidPhoneError(Exception):
    def __init__(self):
        super().__init__("Invalid phone number. phone number must start with 09 and maximum 11 characters.")
        
class InvalidPointError(Exception):
    def __init__(self):
        super().__init__("Invalid point, point must be less or equal 5 and more than 0.")


class UsernameTakenError(Exception):
    def __init__(self):
        super().__init__("The username is already taken.")
        
class AgeLimiteError(Exception):
    def __init__(self):
        super().__init__("age limite for this film!")


class CreateWalletError(Exception):
    def __init__(self):
        super().__init__("A wallet has already been created for the user.")


class WalletNotFound(Exception):
    def __init__(self):
        super().__init__("No wallet with given user id.")


class NotEnoughBalance(Exception):
    def __init__(self):
        super().__init__("Withdrawal amount is more than balance.")


class FilmNotFount(Exception):
    def __init__(self):
        super().__init__("Film not found!")


class RemoveFilmNotPossible(Exception):
    def __init__(self):
        super().__init__("It is not possible to delete the film because the screen is defined for it!")


class RemoveScreenNotPossible(Exception):
    def __init__(self):
        super().__init__("It is not possible to delete the screen because the session is defined for it!")


class UpdateScreenNotPossible(Exception):
    def __init__(self):
        super().__init__("It is not possible to update the screen because the number of defined sessions are more!")


class RemoveSessionNotPossible(Exception):
    def __init__(self):
        super().__init__("The session cannot be deleted because there are reserved seats for this session!")


class CreateSessionNotPossible(Exception):
    def __init__(self):
        super().__init__("It is not possible to create a session because there is another session with the same time for the same screen!")


class CreateSessionNotPossibleCapacity(Exception):
    def __init__(self):
        super().__init__("It is not possible to create a session because capacity not acceptable!")


class CreateSessionNotPossibleMaxNumber(Exception):
    def __init__(self):
        super().__init__("It is not possible to create a session because maximum number of sessions already defined!")


class InvalidCvv2(Exception):
    def __init__(self):
        super().__init__("Entred cvv2 is not valid!")


class InvalidNameForBankAccount(Exception):
    def __init__(self):
        super().__init__("The user already has an account with this name!")


class BankAccountNotFound(Exception):
    def __init__(self):
        super().__init__("Bank account with given user and account name not found!")


class InvalidAccountSecurityInformation(Exception):
    def __init__(self):
        super().__init__("The account security information is incorrect!")


class SeatReserveError(Exception):
    def __init__(self):
        super().__init__("The selected seat cannot be reserved!")


class TicketNotFound(Exception):
    def __init__(self):
        super().__init__("The ticket with given id not found!")
        
class SubscriptionNotFount(Exception):
    def __init__(self):
        super().__init__("The subscription with given name not found!")
        
class WalletBalanceNotEnough(Exception):
    def __init__(self):
        super().__init__("The ticket price is more than your balance!")
        
class CancleTicketNotPossible(Exception):
    def __init__(self):
        super().__init__("The ticket can not be cancle because film session started!")

