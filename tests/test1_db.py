import unittest
from unittest.mock import patch,MagicMock
from queryset import *


##########queryset.py (user _models)
database_manager_instance = MockDatabaseManager.return_value
user_data = {'id': 1, 'username':'testuser' , 'user_name': 'test_user', 'password':'1234567890','email': 'test@example.com', 'birthday': '1990-01-01',
                     'phone': '1234567890', 'subscription_id': 1, 'is_admin': 0}


#add_user_query
add_user_query(user_data)
database_manager_instance.execute_query.assert_called_once_with
(""" INSERT INTO users(id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s) """,user_data)
print("adding users seccesfully")

# test_username_exits_check
def test_username_exits_check(self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        username = 'testuser'
        # Set up the mock return value for execute_query_select
        database_manager_instance.execute_query_select.return_value = [('testuser',)]
        result = username_exits_check(username)
        self.assertEqual(result, [('testuser',)])
print("adding users seccesfully")

# test_change_username_query
def test_username_exits_check(self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        username = 'test_user'
        database_manager_instance.execute_query_select.return_value = [('test_user',)]
        result = change_username_query(username)
        self.assertEqual(result, [('test_user',)])
print("chenging username seccesfully")

# change_password_query
def tchange_password_query(self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        password = '1234567890'
        database_manager_instance.execute_query_select.return_value = [('1234567890',)]
        result = change_password_query(password)
        self.assertEqual(result, [('1234567890',)])
print("chenging password seccesfully")


# email_exist_check_query
def change_password_query(self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        email = 'test@example.com'
        database_manager_instance.execute_query_select.return_value = [('test@example.com',)]
        result = email_exist_check_query (email)
        self.assertEqual(result, [('test@example.com',)])
print("checking for existing email is  seccesfully")

#update_user_phone_query
def update_user_phone_query (self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        phone = '1234567890'
        database_manager_instance.execute_query_select.return_value = [('test@example.com',)]
        result = update_user_phone_query(phone)
        self.assertEqual(result, [('1234567890',)])
print("checking for existing email is  seccesfully")

#add_subscription_query
def add_subscription_query (self, MockDatabaseManager):
        database_manager_instance = MockDatabaseManager.return_value
        add_subcription = '1'
        database_manager_instance.execute_query_select.return_value = [('1',)]
        result =add_subscription_query(add_subcription)
        self.assertEqual(result, [('1',)])
print("adding subscription query is  seccesfully")

##########queryset.py (commend)

# add_film_query
user_data = {'film_name', 'film_age_rating','film_duration' }
add_film_query(user_data)
database_manager_instance.execute_query.assert_called_once_with
(""" INSERT INTO users(id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s) """,user_data)
print("Film added successfully!")

#test_get_films_list_query
mock_database_manager = MagicMock()
queryset.database_manager = mock_database_manager
result = queryset.get_films_list_query()
print(result)

# remove_film_screen_query 
mock_database_manager = MagicMock()
queryset.database_manager = mock_database_manager
result = queryset.remove_film_screen_query()
print(result)

# calculate_point_query
calculate = {'film_id':film_id , 'id' : film_id ,}
calculate_point_query(calculate)
database_manager_instance.execute_query.assert_called_once_with
(""" INSERT INTO users(id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s) """,calculate)
print("calculate calculate points of movie")

# add_comment_query
add_comment = {'comment_film_id' , 'comment_user_id' , 'comment_text' , 'comment_parent_comments_id' }
add_comment_query(add_comment)
database_manager_instance.execute_query.assert_called_once_with
(""" INSERT INTO users(id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s) """,add_comment)
print("comment add seccesfully")

# remove comment
remove_comment = {'comment_id' }
remove_comment_query(remove_comment)
database_manager_instance.execute_query.assert_called_once_with
(""" INSERT INTO users(id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s) """,remove_comment)
print("comment remove seccesfully")

