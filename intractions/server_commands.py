# Exclude run server , other commands handle here:
from users_module.users import Users
from db import models
import getpass


def help_print():
    print("Welcome to server user manual:\n first of all you have to config database")


def signup_admin():
    # all of this need validator its too bad just check when we want to add
    username = input("Enter your desire username:")
    password = getpass.getpass("Enter password: ")
    email = input("Enter your desire email:")
    phone = input("Enter your desire phone:")
    birthday = input("Enter your desire birthday:")
    # Users.AddUser(models.user_model(-1,'Masih32101','masih@abcd1.com','2000-01-01',None,3,'M@@@sih123',is_admin=1))
    # Users.AddUser(models.user_model(-1,'Mohammad961127','mohammadbaharloo96@gmail.com','1996-08-26',"09125397806",3,'Mail1375@#',is_admin=1))

    user = models.user_model(
        -1,
        username=username,
        email=email,
        birthday=birthday,
        phone=phone,
        subscription_type_id=3,
        password=password,
        is_admin=1,
    )
    Users.AddUser(user=user)
    # in database have to check the user is add or not, if add print a successfully add-admin
    print("successfully Add Amin")


def change_user_to_admin(username):
    Users.set_admin(username)



