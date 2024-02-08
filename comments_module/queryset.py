from db.database_manager import DatabaseManager


database_manager = DatabaseManager()


def add_film_query(film_name, film_age_rating, film_duration):
    query = f"""INSERT INTO `films` (`name`, `age_rating`, `duration`, `point`) 
                    VALUES 
                    ('{film_name}', '{film_age_rating}', '{film_duration}', '0');"""
    database_manager.execute_query(query)


def get_film_query(film_id):
    query = f"SELECT id,name,age_rating,duration,point FROM films WHERE id = '{film_id}'"
    r = database_manager.execute_query_select(query)
    return r

def get_films_list_query():
    query = "SELECT id,name,age_rating,duration,point FROM films;"
    r = database_manager.execute_query_select(query)
    return r


def remove_film_screen_query(film_id: int):
    query = f"""SELECT id FROM screens WHERE id = '{film_id}';"""
    r = database_manager.execute_query_select(query)
    return r


def remove_film_films_query(film_id: int):
    query = f"""DELETE FROM films WHERE id = '{film_id}';"""
    database_manager.execute_query(query)


def calculate_point_query(film_id: int) -> None:
    query = f"""UPDATE films set point = (select avg(point) as av from filmspoints  
                    where film_id='{film_id}') 
                    where id = '{film_id}'"""
    database_manager.execute_query(query)


def update_film_query(film_name, film_id, film_age_rating, film_duration):
    query = f"""UPDATE films set 
            name = '{film_name}' AND age_rating = '{film_age_rating}' AND duration = '{film_duration}'
            WHERE id = '{film_id}'"""
    database_manager.execute_query(query)


def select_point_query(user_id: str, film_id: int):
    query = f"SELECT point FROM filmspoints WHERE client_id='{user_id}' AND film_id='{film_id}'"
    r = database_manager.execute_query_select(query)
    return r


def update_point_film(user_id, film_id, point):
    query = f"""UPDATE `filmspoints` SET `point` = '{point}' 
                        WHERE 
                        (`film_id` = '{film_id}') and (`user_id` = '{user_id}');"""
    database_manager.execute_query(query)


def insert_films_point(film_id, user_id, point):
    query = f"""INSERT INTO filmspoints (`{film_id}`, `{user_id}`, `{point}`)
                    VALUES
                    ('{film_id}', '{user_id}', '{point}');"""
    database_manager.execute_query(query)


def remove_point_query(client_id: str, film_id: int):
    query = f"""DELETE FROM filmspoints WHERE user_id = '{client_id}' AND film_id = '{film_id}';"""
    database_manager.execute_query(query)


def add_comment_query(comment_film_id, comment_user_id, comment_text, comment_parent_comments_id):
    query = f"""INSERT INTO `comments` 
            (`film_id`,`user_id`, `text` , `parent_comment`) 
            VALUES 
            ('{comment_film_id}', '{comment_user_id}', '{comment_text}',{comment_parent_comments_id});"""

    database_manager.execute_query(query)


def remove_comment_query(comment_id):
    query = f"""DELETE FROM comments WHERE id = '{comment_id}';"""
    database_manager.execute_query(query)
    return None


def update_comment_query(film_id, user_id, text, parent_comments_id, comment_id):
    query = f"""UPDATE `comments` 
                SET 
                `film_id` = '{film_id}', `user_id` = '{user_id}', 
                `text` = '{text}', `parent_comment` = {parent_comments_id}
                WHERE (`id` = '{comment_id}');"""
    database_manager.execute_query(query)


def get_comments_of_film_query(film_id):
    query = f"""SELECT users.user_name,comments.id,comments.text,comments.created_at,comments.parent_comment 
                    FROM cinemaswift.comments
                    left join cinemaswift.users
                    ON users.id = comments.user_id
                    where comments.film_id = '{film_id}'"""
    result = database_manager.execute_query_select(query)
    return result
