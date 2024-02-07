from db.database_manager import DatabaseManager


database_manager = DatabaseManager()


def create_screen_query(film_id, number_of_screens):
    query = f"""INSERT INTO `screens` (`film_id`, `number_of_sans`) 
            VALUES 
            ('{film_id}', '{number_of_screens}');"""
    database_manager.execute_query(query)


def find_session_id_query(screen_id):
    query = f"""SELECT id FROM sessions WHERE screen_id = '{screen_id}';"""
    r = database_manager.execute_query_select(query)
    return r


def remove_screen_query(screen_id):
    query = f"""DELETE FROM `cinemaswift`.`screens` WHERE (`id` = '{screen_id}');"""
    database_manager.execute_query(query)


def count_session_query(screen_id):
    query = f"""SELECT count(id) FROM sessions WHERE screen_id = '{screen_id}'"""
    r = database_manager.execute_query_select(query)
    return r

def update_screen_query(film_id, number_of_screens, screen_id):
    query = f"""UPDATE `screens`
                    SET `film_id` = '{film_id}', `number_of_sans` = '{number_of_screens}' 
                    WHERE 
                    (`id` = '{screen_id}');"""
    database_manager.execute_query(query)


def get_screen_list_query():
    query = """SELECT cinemaswift.films.name , cinemaswift.screens.number_of_sans FROM cinemaswift.screens
                    join films
                    on  films.id = screens.film_id;"""
    r = database_manager.execute_query_select(query)


def get_screens_list_for_a_film_query(film_id):
    query = f"""SELECT cinemaswift.films.name , cinemaswift.screens.number_of_sans FROM cinemaswift.screens
                    join films
                    on  films.id = screens.film_id
                    WHERE cinemaswift.screens.film_id = '{film_id}';"""
    r = database_manager.execute_query_select(query)


def number_sans_query(screen_id):
    query = f"""SELECT number_of_sans FROM screens 
        WHERE id = '{screen_id}'"""
    total_allowed_sessions = database_manager.execute_query_select(query)
    return total_allowed_sessions


def find_by_start_time_query(timestamp_str):
    query = f"""SELECT id FROM sessions
                     WHERE start_time = '{timestamp_str}';"""
    r = database_manager.execute_query_select(query)
    return r


def insert_session_query(screen_id, timestamp_str, capacity, ticket_price):
    query = f"""INSERT INTO `sessions` (`screen_id`, `start_time`, `capacity` , `ticket_price`) 
                        VALUES 
                        ('{screen_id}', '{timestamp_str}' , '{capacity}' , '{ticket_price}');"""
    database_manager.execute_query(query)


def find_by_time_and_screen_id_query(timestamp_str, screen_id):
    query = f"""SELECT id FROM sessions WHERE start_time = '{timestamp_str}' AND screen_id = '{session.screen_id}'"""
    session_id = database_manager.execute_query_select(query)


def find_total_seats_query(session_id):
    query = f"""SELECT capacity FROM sessions
                    WHERE id = '{session_id}' ;"""
    total_seats = database_manager.execute_query_select(query)[0][0]


def delete_session_query(session_id):
    query = f"""DELETE FROM `sessions` WHERE (`id` = '{session_id}');"""
    database_manager.execute_query(query)


def find_remain_session(screen_id):
    query = f"""SELECT * FROM cinemaswift.sessions
                    WHERE
                    screen_id = '{screen_id}';"""
    r = database_manager.execute_query_select(query)


def create_seat_query(session_id, status, number):
    query = """INSERT INTO `seats` (`session_id`, `status` , `number`) 
                    VALUES """
    for i in range(number):
        query += f"('{session_id}' , '{status}', '{i + 1}'),"
    query = query[:-1] + ';'
    database_manager.execute_query(query)


def update_seat_query(seat_id, status):
    query = f"""UPDATE `cinemaswift`.`seats` SET `status` = '{status.value}' WHERE (`id` = '{seat_id}');"""
    database_manager.execute_query(query)


def get_seats_of_a_session_query(session_id):
    query = f"""SELECT * FROM cinemaswift.seats WHERE session_id = '{session_id}';"""
    r = database_manager.execute_query_select(query)
    return r


def get_number_of_free_seats_query(session_id, seat_type):
    query = f"""SELECT count(id) FROM cinemaswift.seats 
                    WHERE 
                    session_id = '{session_id}' AND status = '{seat_type}';"""
    r = database_manager.execute_query_select(query)
    r = r[0][0]
    return r