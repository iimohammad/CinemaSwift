from db.database_manager import DatabaseManager


database_manager = DatabaseManager()


def select_seat_query(seat_id):
    query = f"""SELECT status FROM seats
                    WHERE id = '{seat_id}';"""
    r = database_manager.execute_query_select(query)


def find_seat_price_query(seat_id):
    query = f"""SELECT ticket_price FROM sessions
            WHERE id = 
                (SELECT session_id FROM seats WHERE id = '{seat_id}');"""

    price = database_manager.execute_query_select(query)[0][0]
    return price


def find_reserve_seat_query(ticket_id):
    query = f"""SELECT seat_id,user_id,price FROM tickets
                    WHERE id = '{ticket_id}';"""
    r = database_manager.execute_query_select(query)
    return r


def delete_reserve_ticket(ticket_id):
    query = f"""DELETE FROM `tickets` WHERE (`id` = '{ticket_id}');"""
    database_manager.execute_query(query)


def find_start_session_time_query(ticket_id):
    query = f"""SELECT start_time FROM sessions 
                    WHERE id = 
                        (SELECT session_id FROM seats WHERE id =
                            (SELECT seat_id FROM cinemaswift.tickets WHERE id = '{ticket_id}'))"""
    result = database_manager.execute_query_select(query)
    return result


def add_buy_ticket_query(user_id, seat_id, price):
    query = f"""INSERT INTO `tickets` (`user_id`, `seat_id`, `price`) 
                    VALUES 
                    ('{user_id}', '{seat_id}', '{price}');"""
    database_manager.execute_query(query)
    
def show_all_tickets_by_user_query(user_id):
    query = f"""select films.name , sessions.start_time , seats.number from tickets
                join seats on tickets.seat_id = seats.id
                join sessions on seats.session_id = sessions.id
                join screens on screens.id = sessions.screen_id
                join films on screens.film_id = films.id
                where tickets.user_id = '{user_id}';"""
    return database_manager.execute_query_select(query)