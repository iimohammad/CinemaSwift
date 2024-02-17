from db.database_manager import DatabaseManager
from users_module import personalized_exceptions
from datetime import datetime

database_manager = DatabaseManager()


def add_user_query(user_data: object) -> None:
    insert_query = """
                    INSERT INTO users
                    (id, user_name, email, birthday, phone , subscription_type_id,  password , is_admin)
                    VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s,%(subscription_type_id)s, %(password)s , %(is_admin)s)
                    """
    database_manager.execute_query(insert_query, user_data)
def get_user_id_by_username_query(username:str):
    query = f"""SELECT id from users 
            WHERE username = '{username}';""" 
    r = database_manager.execute_query_select(query)
    return r[0][0]

def username_exits_check(username):
    query = f"""
                SELECT user_name
                FROM users
                WHERE user_name = '{username}';
                """

    r = database_manager.execute_query_select(query)
    return r


def change_username_query(user_id: str, user_name: str) -> None:
    query = f"""
                UPDATE `cinemaswift`.`users` 
                SET `user_name` = '{user_name}' 
                WHERE (`id` = '{user_id}');
                """
    database_manager.execute_query(query)


def change_password_query(user_id: str, password: str) -> None:
    query = """
        UPDATE users
        SET password = %(password)s
        WHERE id = %(user_id)s;
    """
    data = {'password': password, 'user_id': user_id}
    database_manager.execute_query(query, data)


def email_exist_check_query(email):
    query = f"""
                SELECT email
                FROM users
                WHERE email = '{email}'
                """
    r = database_manager.execute_query_select(query)
    return r


def update_user_email_query(user_id, email):
    query = f"""
                UPDATE users
                SET email = '{email}'
                WHERE id = '{user_id}';
            """
    database_manager.execute_query(query)


def update_user_phone_query(user_id, phone):
    query = f"""
                UPDATE users
                SET phone = '{phone}'
                WHERE id = '{user_id}';
            """
    database_manager.execute_query(query)


def update_last_login_query(user_id):
    query = f"""UPDATE users SET last_login = '{
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
    database_manager.execute_query(query)


def get_user_birthday_query(user_id) -> datetime:
    query = f"""SELECT birthday FROM cinemaswift.users
            where id = '{user_id}';"""
    r = database_manager.execute_query_select(query)
    return r[0][0]


def login_query(user_name):
    query = f"""
                        SELECT id,password FROM users
                        WHERE user_name = '{user_name}'
                    """
    r = database_manager.execute_query_select(query)
    return r


def set_user_as_admin(user_id) -> None:
    query = f"""
            UPDATE users SET is_admin = 1
            WHERE id = {user_id}
            """


def set_user_as_admin_by_username(username) -> None:
    query = f"""
            UPDATE users SET is_admin = 1
            WHERE id = {username}
            """


def add_subscription_query(user_id, subscription_id) -> None:
    query = f"""INSERT INTO `userssubscriptions` (`user_id`, `subscription_id`, `start_date`) 
                    VALUES 
                    ('{user_id}', '{subscription_id}', '{datetime.now()}');"""
    database_manager.execute_query(query)
def change_subscription_query(user_id: str, subscription_type_name: str):
    query = f"""SELECT id FROM subscriptions
                    WHERE name = '{subscription_type_name}';"""
    r = database_manager.execute_query_select(query)
    if len(r) == 0:
        raise personalized_exceptions.SubscriptionNotFount()

    query = f"""UPDATE `users` SET `subscription_type_id` = '{r[0][0]}' 
                    WHERE (`id` = '{user_id}');"""
    database_manager.execute_query(query)


def get_subscription_type_name_query(user_id: str):
    query = f"""SELECT name FROM subscriptions
                    where
                    id = (SELECT subscription_type_id FROM cinemaswift.users where id = '{user_id}');"""
    return database_manager.execute_query_select(query)

def get_subscription_discount_value_query(user_id: str):
    query = f"""SELECT discount_value FROM subscriptions
                    where
                    id = (SELECT subscription_id FROM cinemaswift.userssubscriptions where user_id = '{user_id}');"""
    return database_manager.execute_query_select(query)


def get_subscription_discount_number_query(subscription_name: str):
    query = f"""SELECT discount_number FROM subscriptions
                    WHERE
                    name = '{subscription_name}'"""
    return database_manager.execute_query_select(query)[0][0]


def get_total_discounts_taken_query(user_id: str):
    query = f"""SELECT count(id) FROM tickets
                WHERE created_at >= 
    	        (select start_date FROM userssubscriptions WHERE user_id = '{user_id}')"""
    return database_manager.execute_query_select(query)[0][0]


def get_subscription_start_date_query(user_id: str):
    query = f"""SELECT start_date FROM userssubscriptions
            WHERE user_id = '{user_id}';"""
    return database_manager.execute_query_select(query)[0][0]


def is_admin_check_query(user_id):
    query = f"""
        SELECT is_admin FROM users
        WHERE id = '{user_id}';
        """
    r = database_manager.execute_query_select(query)
    if r[0][0] == 1:

        return True
    return False


def show_profile_query(user_id: str) -> dict:
    query = f"""
        SELECT users.user_name,users.email,users.birthday,users.phone,subscriptions.name,users.created_at FROM cinemaswift.users
        join subscriptions on subscriptions.id = users.subscription_type_id
        where users.id = '{user_id}';
        """
    r = database_manager.execute_query_select(query)
    return {
        'user_name': r[0][0],
        'email': r[0][1],
        'birthday': r[0][2],
        'phone': r[0][3],
        'subscription_type': r[0][4],
        'created_at': r[0][5],
    }
