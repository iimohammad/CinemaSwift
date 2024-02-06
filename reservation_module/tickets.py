from screen_module import screens
from db.database_manager import DatabaseManager
<<<<<<< HEAD
from users_module import personalized_exceptions
from datetime import datetime
=======
import personalized_exceptions
from datetime import datetime , timedelta
from payment_module.wallet import Wallets
from users_module.users import Subscriptions
from db.models import SubscriptopnType
>>>>>>> main
class Ticket:
    database_manager = DatabaseManager()
    
    @staticmethod
    def buy_ticket(user_id:str , seat_id:int)->bool:
        """
    Purchase a ticket for a user and seat, considering subscription discounts and balance.

    Args:
        user_id (str): The unique identifier of the user.
        seat_id (int): The identifier of the seat to be purchased.

    Returns:
        bool: True if the ticket is successfully purchased, False otherwise.

    Raises:
        personalized_exceptions.SeatReserveError: If the seat is already reserved.
        personalized_exceptions.WalletBalanceNotEnough: If the user's wallet balance is insufficient.

    Notes:
        This function performs the following actions:
        1. Checks the status of the seat; raises an exception if it's already reserved.
        2. Retrieves the ticket price based on the session and applies subscription discounts.
        3. Checks the user's wallet balance and raises an exception if it's not enough.
        4. Inserts the ticket information into the database and updates the seat status to 'RESERVED'.
        5. If the user has a Golden subscription for more than 30 days, changes it to Bronze.
        6. If the user has a Silver subscription and reached the discount limit, changes it to Bronze.

    """
        query = f"""SELECT status FROM cinemaswift.seats
                WHERE id = '{seat_id}';"""
        r = Ticket.database_manager.execute_query_select(query)
        
        if r[0][0] == screens.SeatType.RESERVED.value:
            raise personalized_exceptions.SeatReserveError()
        
        query = f"""SELECT ticket_price FROM cinemaswift.sessions
                WHERE id = 
                    (SELECT session_id FROM cinemaswift.seats WHERE id = '{seat_id}');"""
        
        price = Ticket.database_manager.execute_query_select(query)[0][0]
        wallet_balance = Wallets.get_balance(user_id)
        subscriptopn_type = Subscriptions.get_subscription_type_name(user_id)
        if subscriptopn_type==SubscriptopnType.Golden.value:
            start_date = Subscriptions.get_subscription_start_date(user_id)
            date_format = '%Y-%m-%d %H:%M:%S'
            converted_datetime  = datetime.strptime(start_date, date_format)
            if converted_datetime-datetime.now() > timedelta(days=30):
                Subscriptions.change_subscription(user_id,SubscriptopnType.Bronze.value)
        subscriptopn_discount_value = Subscriptions.get_subscription_discount_value(subscriptopn_type)
        if subscriptopn_type != SubscriptopnType.Bronze.value:
            price = round(price*(subscriptopn_discount_value/100),1)
        if price > wallet_balance:
            raise personalized_exceptions.WalletBalanceNotEnough()
        
        query = f"""INSERT INTO `cinemaswift`.`tickets` (`user_id`, `seat_id`, `price`) 
                VALUES 
                ('{user_id}', '{seat_id}', '{price}');"""
        Ticket.database_manager.execute_query(query)
        screens.Seats.update_seat(seat_id,screens.SeatType.RESERVED)
        
        if (subscriptopn_type==SubscriptopnType.Silver.value):
            discount_nubmer = Subscriptions.get_subscription_discount_number(SubscriptopnType.Silver.value)
            discount_nubmers_taken = Subscriptions.get_total_discounts_taken(user_id)
            if discount_nubmer==discount_nubmers_taken:
                Subscriptions.change_subscription(user_id,SubscriptopnType.Bronze.value)
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
        query = f"""SELECT seat_id,user_id,price FROM cinemaswift.tickets
                WHERE id = '{ticket_id}';"""
        r = Ticket.database_manager.execute_query_select(query)
        if len(r)==0:
            raise personalized_exceptions.TicketNotFound()
        seat_id = r[0][0]
        user_id = r[0][1]
        price = r[0][2]
        query = f"""DELETE FROM `cinemaswift`.`tickets` WHERE (`id` = '{ticket_id}');"""
        Ticket.database_manager.execute_query(query)
        screens.Seats.update_seat(seat_id,screens.SeatType.FREE)
        Wallets.deposit_to_wallet(user_id,price)
        return r[0][1]