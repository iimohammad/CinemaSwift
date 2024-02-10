import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from reservation_module.tickets import Ticket
from users_module.users import personalized_exceptions

class TestTicket(unittest.TestCase):

    @patch('reservation_module.queryset.select_seat_query')
    @patch('reservation_module.queryset.find_seat_price_query')
    @patch('reservation_module.queryset.add_buy_ticket_query')
    @patch('reservation_module.queryset.find_reserve_seat_query')
    @patch('reservation_module.queryset.show_all_tickets_by_user_query')
    def test_buy_ticket(self, mock_show_all_tickets_by_user_query, mock_find_reserve_seat_query,
                        mock_add_buy_ticket_query, mock_find_seat_price_query, mock_select_seat_query):
        mock_select_seat_query.return_value = [('RESERVED',)]
        mock_find_seat_price_query.return_value = 100
        mock_show_all_tickets_by_user_query.return_value = []
        user_id = 'user1'
        seat_id = 1
        with patch('users_module.users.Subscriptions') as mock_subscriptions, \
                patch('users_module.users.Users') as mock_users, \
                patch('payment_module.wallet.Wallets') as mock_wallets, \
                patch('screen_module.screens.Seats') as mock_seats:
            mock_subscriptions.get_subscription_type_name.return_value = 'Silver'
            mock_users.get_user_birthday.return_value = datetime.now().date()
            mock_subscriptions.get_subscription_discount_value.return_value = 10
            mock_wallets.get_balance.return_value = 120
            self.assertTrue(Ticket.buy_ticket(user_id, seat_id))
            mock_add_buy_ticket_query.assert_called_once_with(user_id, seat_id, 100)
            mock_seats.update_seat.assert_called_once_with(seat_id, 'RESERVED')
            mock_wallets.deposit_to_wallet.assert_not_called()

    @patch('reservation_module.queryset.find_start_session_time_query')
    @patch('reservation_module.queryset.find_reserve_seat_query')
    @patch('reservation_module.Ticket.remaine_time_session')
    def test_cancel_ticket(self, mock_remaine_time_session, mock_find_reserve_seat_query, mock_find_start_session_time_query):
        mock_remaine_time_session.return_value = 120
        mock_find_reserve_seat_query.return_value = [(1, 'user1', 100)]
        ticket_id = 1
        with patch('reservation_module.queryset.delete_reserve_ticket'), \
             patch('screen_module.screens.Seats') as mock_seats, \
             patch('payment_module.Wallets') as mock_wallets:
            self.assertEqual(Ticket.cancel_ticket(ticket_id), 'user1')
            mock_seats.update_seat.assert_called_once_with(1, 'FREE')
            mock_wallets.deposit_to_wallet.assert_called_once_with('user1', 100)

    @patch('reservation_module.queryset.find_start_session_time_query')
    def test_remaine_time_session(self, mock_find_start_session_time_query):
        mock_find_start_session_time_query.return_value = [(datetime.now() + timedelta(minutes=30),)]
        ticket_id = 1
        self.assertEqual(Ticket.remaine_time_session(ticket_id), 30)

    @patch('reservation_module.queryset.show_all_tickets_by_user_query')
    def test_show_all_tickets_by_user(self, mock_show_all_tickets_by_user_query):
        mock_show_all_tickets_by_user_query.return_value = [(1, datetime.now(), 100)]
        user_id = 'user1'
        self.assertEqual(Ticket.show_all_tickets_by_user(user_id), [[1, datetime.now(), 100]])

    @patch('reservation_module.queryset.show_all_tickets_by_user_query')
    def test_show_all_past_tickets_by_user(self, mock_show_all_tickets_by_user_query):
        mock_show_all_tickets_by_user_query.return_value = [(1, datetime.now() - timedelta(days=1), 100)]
        user_id = 'user1'
        self.assertEqual(Ticket.show_all_past_tickets_by_user(user_id), [[1, datetime.now() - timedelta(days=1), 100]])

if __name__ == '__main__':
    unittest.main()
