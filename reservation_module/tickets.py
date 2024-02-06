from screen_module import screens
from db.database_manager import DatabaseManager
from users_module import personalized_exceptions
from datetime import datetime
class Ticket:
    database_manager = DatabaseManager()
    
    @staticmethod
    def buy_ticket(user_id:str , seat_id:int , price:int)->bool:
        """
    Purchase a ticket for a specific seat.

    Args:
        user_id (str): The ID of the user buying the ticket.
        seat_id (int): The ID of the seat for which the ticket is being purchased.
        price (int): The price of the ticket.

    Returns:
        bool: True if the ticket purchase is successful; otherwise, False.

    Raises:
        personalized_exceptions.SeatReserveError: If the selected seat is already reserved.
    """
        query = f"""SELECT status FROM cinemaswift.seats
                WHERE id = '{seat_id}';"""
        r = Ticket.database_manager.execute_query_select(query)
        
        if r[0][0] == screens.SeatType.RESERVED.value:
            raise personalized_exceptions.SeatReserveError()
        query = f"""INSERT INTO `cinemaswift`.`tickets` (`user_id`, `seat_id`, `price`) 
                VALUES 
                ('{user_id}', '{seat_id}', '{price}');"""
        Ticket.database_manager.execute_query(query)
        screens.Seats.update_seat(seat_id,screens.SeatType.RESERVED)
        return True
    @staticmethod
    def ramain_time_to_sesstion_by_minutes(ticket_id:int) -> int:
        """
    Calculate the remaining time to the session associated with a given ticket in minutes.

    Args:
        ticket_id (int): The ID of the ticket.

    Returns:
        int: The remaining time to the session in minutes.

    Raises:
        personalized_exceptions.TicketNotFound: If the specified ticket ID is not found.
    """
        query = f"""SELECT start_time FROM sessions 
                WHERE id = 
                    (SELECT session_id FROM seats WHERE id =
                        (SELECT seat_id FROM cinemaswift.tickets WHERE id = '{ticket_id}'))"""
        r = Ticket.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.TicketNotFound()
        
        time_difference =  r[0][0] - datetime.now()
        return int(time_difference.total_seconds() // 60)
    @staticmethod
    def cancel_ticket(ticket_id:int)->float:
        """
    Cancel a previously purchased ticket and free up the associated seat.

    Args:
        ticket_id (int): The ID of the ticket to be canceled.

    Returns:
        float: The price of the canceled ticket.

    Raises:
        personalized_exceptions.TicketNotFound: If the specified ticket ID is not found.
    """
        query = f"""SELECT seat_id,price FROM cinemaswift.tickets
                WHERE id = '{ticket_id}';"""
        r = Ticket.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.TicketNotFound()
        seat_id = r[0][0]
        query = f"""DELETE FROM `cinemaswift`.`tickets` WHERE (`id` = '{ticket_id}');"""
        Ticket.database_manager.execute_query(query)
        screens.Seats.update_seat(seat_id,screens.SeatType.FREE)
        return r[0][1]