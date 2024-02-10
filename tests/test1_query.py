import unittest
from datetime import date
from db.database_manager import DatabaseManager
from queryset import*

database_manager = DatabaseManager()

def add_user_query():
    user_data = {
        "id": input(" "),
        "user_name":input(" "),
        "email": input(" "),
        "birthday":input(" "),
        "phone": input(" "),
        "subscription_type_id": input(" "),
        "password": input(" "),
    }

    print("Testing add_user_query:")
    add_user_query(user_data)
    print("User added successfully.")

def username_exits_check():
    username_to_check = input("")
    print("\nTesting username_exits_check:")
    result = username_exits_check(username_to_check)
    print(f"Username '{username_to_check}' exists: {result}")

def change_username_query():
    user_id_to_change = input("")
    new_username = input("")
    print("\nTesting change_username_query:")
    change_username_query(user_id_to_change, new_username)
    print(f"Username changed successfully for user with ID {user_id_to_change} to '{new_username}'.")

# Test change_password_query
    
def change_password_query():
    user_id_to_change_password = input("")
    new_password = input("")
    print("\nTesting change_password_query:")
    change_password_query(user_id_to_change_password, new_password)
    print(f"Password changed successfully for user with ID {user_id_to_change_password}.")

# Test email_exist_check_query  
def email_exist_check_query():
    email_to_check = "test_user@example.com"
    print("\nTesting email_exist_check_query:")
    result = email_exist_check_query(email_to_check)
    print(f"Email '{email_to_check}' exists: {result}")

# Test update_last_login_query  
def update_last_login_query():
    user_id_for_last_login = input("")
    print("\nTesting update_last_login_query:")
    update_last_login_query(user_id_for_last_login)
    print(f"Last login updated for user with ID {user_id_for_last_login}.")

# Test get_user_birthday_query
def get_user_birthday_query():
    user_id_for_birthday = input("")
    print("\nTesting get_user_birthday_query:")
    user_birthday = get_user_birthday_query(user_id_for_birthday)
    print(f"Birthday for user with ID {user_id_for_birthday}: {user_birthday}")

# Test login_query
def login_query():
    username_to_login = "test_user"
    print("\nTesting login_query:")
    login_result = login_query(username_to_login)
    print(f"Login result for user '{username_to_login}': {login_result}")


# Test change_subscription_query
def change_subscription_query():
    user_id_for_subscription = "3"
    subscription_type_to_change = "New Subscription"
    print("\nTesting change_subscription_query:")
    change_subscription_query(user_id_for_subscription, subscription_type_to_change)
    print(f"Subscription changed for user with ID {user_id_for_subscription}.")

# Test is_admin_check_query
def is_admin_check_query():
    user_id_for_admin_check = "4"
    print("\nTesting is_admin_check_query:")
    isAdmin = is_admin_check_query(user_id_for_admin_check)
    print(f"Is user with ID {user_id_for_admin_check} an admin: {isAdmin}")

# Test show_profile_query
def is_admin_check_query():
    user_id_for_profile = "5"
    print("\nTesting show_profile_query:")
    user_profile = is_admin_check_query()(user_id_for_profile)
    print(f"User profile for user with ID {user_id_for_profile}: {user_profile}")

# Run the tests
add_user_query()
username_exits_check()
change_username_query()
change_password_query()
email_exist_check_query()
update_last_login_query()
get_user_birthday_query()
login_query()
change_subscription_query()
is_admin_check_query()
is_admin_check_query()