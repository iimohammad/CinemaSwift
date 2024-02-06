from db.database_manager import DatabaseManager
from users_module import personalized_exceptions
from datetime import datetime

database_manager = DatabaseManager()


def add_user_query(user_data: object) -> None:
    insert_query = """
                    INSERT INTO users
                    (id, user_name, email, birthday, phone,  password)
                    VALUES (%(id)s, %(user_name)s, %(email)s, %(birthday)s, %(phone)s, %(password)s)
                    """
    database_manager.execute_query(
        insert_query, user_data)


def username_exits_check(username):
    query = f"""
                SELECT user_name
                FROM users
                WHERE user_name = '{username}'
                UNION
                SELECT "user_name"
                FROM admins
                WHERE user_name = '{username}';
                """

    r = database_manager.execute_query_select(query)
    return r


def email_exist_check(email):
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


def set_created_at(user_id) -> None:
    query = f"""UPDATE users SET created_at = '{
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = '{user_id}'"""
    database_manager.execute_query(query)


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


def add_subscription_query(user_id, subscription_id) -> None:
    query = f"""INSERT INTO `cinemaswift`.`userssubscriptions` (`user_id`, `subscription_id`, `start_date`) 
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
    return database_manager.execute_query_select(query)[0][0]


def get_subscription_discount_number_query(subscription_name: str):
    query = f"""SELECT discount_number FROM cinemaswift.subscriptions
                    WHERE
                    name = '{subscription_name}'"""
    return database_manager.execute_query_select(query)[0][0]


def get_total_discounts_taken_query(user_id: str):
    query = f"""SELECT count(id) FROM cinemaswift.tickets
                WHERE created_at >= 
    	        (select start_date FROM userssubscriptions WHERE user_id = '{user_id}')"""
    return database_manager.execute_query_select(query)[0][0]


def get_subscription_start_date_query(user_id: str):
    query = f"""SELECT start_date FROM cinemaswift.userssubscriptions
            WHERE user_id = '{user_id}';"""
    return database_manager.execute_query_select(query)[0][0]
