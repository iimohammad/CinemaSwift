class ShortPasswordError(Exception):
    def __init__(self, password_length, minimum_length):
        super().__init__(f"Password must be at least {minimum_length} characters long, but got {password_length} characters.")

class NoSpecialCharacterError(Exception):
    def __init__(self):
        super().__init__("Password must contain at least three special character (# , @ , & , &).")

class ComplexityError(Exception):
    def __init__(self):
        super().__init__("Must contain Uppercase and lowercase letters and numbers.")
        
class LongUserNmaeError(Exception):
    def __init__(self,user_name_length, maximum_length):
        super().__init__(f"User name must be less or equal {maximum_length} characters long, but got {user_name_length} characters.")

class InvalidEmailError(Exception):
    def __init__(self):
        super().__init__("Invalid email address.")
        
class InvalidPhoneError(Exception):
    def __init__(self):
        super().__init__("Invalid phone number. phone number must start with 09 and maximum 11 characters.")
class UsernameTakenError(Exception):
    def __init__(self):
        super().__init__("The username is already taken.")
        
class CreateWalletError(Exception):
    def __init__(self):
        super().__init__("A wallet has already been created for the user.")

class WalletNotFound(Exception):
    def __init__(self):
        super().__init__("No wallet with given user id.")
        
class NotEnoughBalance(Exception):
    def __init__(self):
        super().__init__("Withdrawal amount is more than balance.")