class ShortPasswordError(Exception):
    """
    Exception raised when the password provided is too short.

    Attributes:
        password_length (int): The length of the provided password.
        minimum_length (int): The minimum required length for the password.
    """
    def __init__(self, password_length, minimum_length):
        super().__init__(f"Password must be at least {
            minimum_length} characters long, but got {password_length} characters.")


class NoSpecialCharacterError(Exception):
    """
    Exception raised when the password does not contain enough special characters.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Password must contain at least three special character (# , @ , & , &).")


class ComplexityError(Exception):
    """
    Exception raised when the password does not meet complexity requirements.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Must contain Uppercase and lowercase letters and numbers.")


class LongUserNmaeError(Exception):
    """
    Exception raised when the username provided is too long.

    Attributes:
        user_name_length (int): The length of the provided username.
        maximum_length (int): The maximum allowed length for the username.
    """
    def __init__(self, user_name_length, maximum_length):
        super().__init__(f"User name must be less or equal {
            maximum_length} characters long, but got {user_name_length} characters.")


class InvalidEmailError(Exception):
    """
    Exception raised when an invalid email address is provided.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Invalid email address.")


class InvalidPhoneError(Exception):
    """
    Exception raised when an invalid phone number is provided.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Invalid phone number. phone number must start with 09 and maximum 11 characters.")


class UsernameTakenError(Exception):
    """
    Exception raised when the provided username is already taken.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The username is already taken.")


class CreateWalletError(Exception):
    """
    Exception raised when a wallet has already been created for the user.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("A wallet has already been created for the user.")


class WalletNotFound(Exception):
    """
    Exception raised when no wallet is found for the given user ID.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("No wallet with given user id.")


class NotEnoughBalance(Exception):
    """
    Exception raised when the withdrawal amount exceeds the balance.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Withdrawal amount is more than balance.")


class FilmNotFount(Exception):
    """
    Exception raised when a film is not found.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Film not found!")


class RemoveFilmNotPossible(Exception):
    """
    Exception raised when it is not possible to delete a film.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to delete the film because the screen is defined for it!")


class RemoveScreenNotPossible(Exception):
    """
    Exception raised when it is not possible to delete a screen.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to delete the screen because the session is defined for it!")


class UpdateScreenNotPossible(Exception):
    """
    Exception raised when it is not possible to update a screen.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to update the screen because the number of defined sessions are more!")


class RemoveSessionNotPossible(Exception):
    """
    Exception raised when it is not possible to remove a session.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The session cannot be deleted because there are reserved seats for this session!")


class CreateSessionNotPossible(Exception):
    """
    Exception raised when it is not possible to create a session.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to create a session because there is another session with the same time for the same screen!")


class CreateSessionNotPossibleCapacity(Exception):
    """
    Exception raised when it is not possible to create a session due to capacity constraints.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to create a session because capacity not acceptable!")


class CreateSessionNotPossibleMaxNumber(Exception):
    """
    Exception raised when it is not possible to create a session due to reaching the maximum number of sessions.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("It is not possible to create a session because maximum number of sessions already defined!")


class InvalidCvv2(Exception):
    """
    Exception raised when an invalid CVV2 is provided.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Entred cvv2 is not valid!")


class InvalidNameForBankAccount(Exception):
    """
    Exception raised when an invalid name is provided for a bank account.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The user already has an account with this name!")


class BankAccountNotFound(Exception):
    """
    Exception raised when a bank account is not found.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("Bank account with given user and account name not found!")


class InvalidAccountSecurityInformation(Exception):
    """
    Exception raised when invalid security information is provided for an account.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The account security information is incorrect!")


class SeatReserveError(Exception):
    """
    Exception raised when it is not possible to reserve a seat.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The selected seat cannot be reserved!")


class TicketNotFound(Exception):
    """
    Exception raised when a ticket is not found.

    Attributes:
        None
    """
    def __init__(self):
        super().__init__("The ticket with given id not found!")
