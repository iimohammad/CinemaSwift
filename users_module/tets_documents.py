
import unittest
from users import*


class BaseForUsersAndAdmins(unittest.TestCase):

    def _hashPassword(self):
        # Valid input
        password = input("")
        hashed_password = BaseForUsersAndAdmins._hashPassword (password)
        self.assertIsNotNone(hashed_password)
        print("Hashed Password :" , hashed_password)

    
    def _phoneValidator(self):
        # Valid input
        phone = input(" ")
        result = BaseForUsersAndAdmins._phoneValidator(phone)
        self.assertTrue(result)
        print("Valid Phone Number:", phone)
        
    def PasswordValidator(self):
        password = input("")
        result = BaseForUsersAndAdmins.PasswordValidator(password)
        self.assertTrue(result)
        print("Valid Password:", password)

    def UserNameValidator(self):
        username = input("")
        result = BaseForUsersAndAdmins._UserNameValidator(username)
        self.assertTrue(result)
        print("Valid Username:", username)

   
    def _emailValidatorUser(self):
        email = input("")
        result = Users._emailValidatorUser(email)
        self.assertTrue(result)
        print("Valid Email:", email)

    def AddUser(self):
        user = input("")
        result = Users.AddUser(user)
        self.assertTrue(result)
        print("Valid User:", user)
    

    def updateUserEmail(self):
        UserEmail = input("")
        result = Users.updateUserEmail(UserEmail)
        self.assertTrue(result)
        print("Valid UserEmail:", UserEmail)

   
    def updateUserPhone(self):
        UserPhone = input("")
        result = Users.updateUserPhone(UserPhone)
        self.assertTrue(result)
        print("Valid UserPhone:", UserPhone)

    def _update_last_login(self):
        last_login = input("")
        result = Users._update_last_login(last_login)
        self.assertTrue(result)
        print("last_login:", last_login)

    def log_in(self):
        login = input("")
        result = Users.log_in(login)
        self.assertTrue(result)
        print("login:", login)

    
    def _emailValidatorAdmin(self):
        email_Admin = input("")
        result = Admins._emailValidatorUser(email_Admin)
        self.assertTrue(result)
        print("email_Admin:", email_Admin)

    def AddAdmin(self):
        AddAdmin = input("")
        result = Admins.AddUser(AddAdmin)
        self.assertTrue(result)
        print("Adress:", AddAdmin)
    

    def updateAdminUserName(self):
        Update_Admin_username = input("")
        result = Admins.updateUserEmail(Update_Admin_username)
        self.assertTrue(result)
        print("Admin username:", Update_Admin_username)

    def updateAdminEmail(self):
        Update_Admin_Email = input("")
        result = Admins.updateUserEmail(Update_Admin_Email)
        self.assertTrue(result)
        print("Admin Email:", Update_Admin_Email)

    def updateAdminPhone(self):
        Update_Admin_Phone = input("")
        result = Admins.updateUserEmail(Update_Admin_Phone)
        self.assertTrue(result)
        print("Admin Phone:", Update_Admin_Phone)

    def  _update_last_login(self):
        update_last_login = input("")
        result = Admins.updateUserEmail(update_last_login)
        self.assertTrue(result)
        print("last_login:", update_last_login)

    def updateAdminUserName(self):
        Update_Admin_username = input("")
        result = Admins.updateUserEmail(Update_Admin_username)
        self.assertTrue(result)
        print("user name:", Update_Admin_username)

    def log_in(self):
        login = input("")
        result = Admins.updateUserEmail(login)
        self.assertTrue(result)
        print("login", login)