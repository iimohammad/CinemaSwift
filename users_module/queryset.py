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
