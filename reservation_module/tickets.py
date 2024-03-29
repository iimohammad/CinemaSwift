from screen_module import screens
from users_module import personalized_exceptions
from screen_module.screens import Seats
from datetime import datetime, timedelta
from payment_module.wallet import Wallets
from users_module.users import Subscriptions, Users
from db.models import SubscriptopnType
from reservation_module import queryset
import os

class Ticket:
    log_file = "ticket.log"
    @classmethod
    def add_log(cls,txt: str):
        if not os.path.exists(cls.log_file):
            with open(cls.log_file, 'w') as f:
                pass
        with open(cls.log_file, 'a') as f:
            f.write(
                txt +
                f""" _ at {
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""" +
                os.linesep)
    @staticmethod
    def buy_ticket(user_id: str, seat_id: int) -> bool:
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
        7. If it is the user's birthday, the user will receive a 50% discount.
    """
        r = queryset.select_seat_query(seat_id)

        if r[0][0] == screens.SeatType.RESERVED.value:
            raise personalized_exceptions.SeatReserveError()

        price = queryset.find_seat_price_query(seat_id)
        wallet_balance = Wallets.get_balance(user_id)
        subscript = Subscriptions.get_subscription_type_name(user_id)

        if subscript == SubscriptopnType.Golden.value:
            start_date = Subscriptions.get_subscription_start_date(user_id)
            if start_date - datetime.now() > timedelta(days=30):
                Subscriptions.change_subscription(user_id, SubscriptopnType.Bronze.value)
        discount_reason = 'SubscriptionType'
        discount_percent = Subscriptions.get_subscription_discount_value(user_id)
        user_birthday = Users.get_user_birthday(user_id)
        age = Users.calculateAge(user_birthday.date())
        film_age_rating = Seats.get_age_rating(seat_id)
        if age<film_age_rating:
            raise personalized_exceptions.AgeLimiteError()
        now = datetime.now().date()
        if user_birthday.day == now.day and user_birthday.month == now.month:
            price = round(price * (50 / 100), 1)
            discount_reason = 'BirthDay'
            
        elif subscript != SubscriptopnType.Bronze.value:
            price = round(price * (discount_percent / 100), 1)
        if price > wallet_balance:
            raise personalized_exceptions.WalletBalanceNotEnough()
        queryset.add_buy_ticket_query(user_id, seat_id, price)

        screens.Seats.update_seat(seat_id, screens.SeatType.RESERVED)

        if subscript == SubscriptopnType.Silver.value:
            discount_number = Subscriptions.get_subscription_discount_number(SubscriptopnType.Silver.value)
            discount_numbers_taken = Subscriptions.get_total_discounts_taken(user_id)
            if discount_number == discount_numbers_taken:
                Subscriptions.change_subscription(user_id, SubscriptopnType.Bronze.value)
        Ticket.add_log(f"""Ticket Buy _ {user_id = } _ {seat_id = } _ 
                       {discount_reason = } _ {discount_percent = } _ 
                       {price = }""")
        return True

    @staticmethod
    def remaine_time_session(ticket_id: int) -> int:
        """
    Calculate the remaining time to the session associated with a given ticket in minutes.
    Args:
        ticket_id (int): The ID of the ticket.
    Returns:
        int: The remaining time to the session in minutes.
    Raises:
        personalized_exceptions.TicketNotFound: If the specified ticket ID is not found.
    """
        r = queryset.find_start_session_time_query(ticket_id)

        if len(r) == 0:
            raise personalized_exceptions.TicketNotFound()

        time_difference = r[0][0] - datetime.now()
        return int(time_difference.total_seconds() // 60)

    @staticmethod
    def cancel_ticket(ticket_id: int) -> float:
        """
    Cancel a previously purchased ticket and free up the associated seat.
    Args:
        ticket_id (int): The ID of the ticket to be canceled.
    Returns:
        float: The price of the canceled ticket.
    Raises:
        personalized_exceptions.TicketNotFound: If the specified ticket ID is not found.
    """
        r = queryset.find_reserve_seat_query(ticket_id)

        if len(r) == 0:
            raise personalized_exceptions.TicketNotFound()

        remain_time = Ticket.remaine_time_session(ticket_id)

        if remain_time < 1:
            raise personalized_exceptions.CancleTicketNotPossible()

        seat_id = r[0][0]
        user_id = r[0][1]
        price = r[0][2]
        cancellation_penalty = 0
        if remain_time < 61:
            price = round(price * (18 / 100), 1)
            cancellation_penalty = 18

        queryset.delete_reserve_ticket(ticket_id)

        screens.Seats.update_seat(seat_id, screens.SeatType.FREE)
        Wallets.deposit_to_wallet(user_id, price)
        Ticket.add_log(f"""Ticket Cancel _ {user_id = } _ {seat_id = } _ 
                       {cancellation_penalty = } _ {price = }""")
        return r[0][1]

    @classmethod
    def show_all_tickets_by_user(cls, user_id:str):
        tickets = []
        r = queryset.show_all_tickets_by_user_query(user_id=user_id)
        for i in r:
            tickets.append([i[0], i[1], i[2], i[3]])
        return tickets

    @classmethod
    def show_all_past_tickets_by_user(cls, user_id: str):
        tickets = []
        r = queryset.show_all_tickets_by_user_query(user_id=user_id)
        for i in r:
            start_time = i[1]
            if start_time < datetime.now():
                tickets.append([i[0], i[1], i[2], i[3]])
        return tickets