from db import models
from payment_module.bankaccounts import BankAccounts
from payment_module.wallet import Wallets
from reservation_module.tickets import Ticket
from users_module.users import Users, Subscriptions


class InteractionsCommands:
    @classmethod
    def change_username_func(cls, username: str, data_dict_command):
        new_username = data_dict_command['username']
        if Users.change_username(username=username, new_username=new_username):
            response = "change username successfully"
            return response

    @classmethod
    def change_password_func(cls, username: str, data_dict_command):
        new_password = data_dict_command['password']
        if Users.change_password(username=username, password=new_password):
            response = "change password successfully"
            return response

    @classmethod
    def change_email_func(cls, username, data_dict_command):
        new_email = data_dict_command['email']
        if Users.change_email(username=username, email=new_email):
            response = "change Email successfully"
            return response

    @classmethod
    def change_phoneNumber(cls, username, data_dict_command):
        new_phone = data_dict_command['phoneNumber']
        if Users.change_phone_number(username=username, phone=new_phone):
            response = "change phone Number successfully"
            return response

    @classmethod
    def show_profile_func(cls, username, data_dict_command):
        Users.show_profile(username=username)

    @classmethod
    def remove_bank_account_func(cls, username, data_dict_command):
        pass
        # BankAccounts.remove_bank_account(name)

    @classmethod
    def show_balance_func(cls, username, data_dict_command):
        Wallets.get_balance_by_username(username)

    @classmethod
    def show_bank_accounts_func(cls, username, data_dict_command):
        BankAccounts.show_all_accounts_by_username(username=username)

    @classmethod
    def show_reservation_func(cls, username, data_dict_command):
        Ticket.show_all_buy_tickets(username=username)

    @classmethod
    def show_subscription_detail_func(cls, username, data_dict_command):
        pass
        # type_subs = Subscriptions.get_subscription_type_name(user_id)
        # if type_subs == 3:
        #     print("options of this Golden subscription is:")
        # elif type_subs == 2:
        #     print("options of this Silver subscription is:")
        # else:
        #     print("options of this Bronze subscription is:")

    @classmethod
    def remove_account_func(cls, username, data_dict_command):
        pass
        # Users.remove_account(user_id)

    @classmethod
    def add_bank_Account_func(cls, username, data_dict_command):
        cvv2 = data_dict_command['cvv2']
        name = data_dict_command['name']

        # BankAccounts.add_bank_account(account)

    @classmethod
    def re_charge_func(cls, username, data_dict_command):
        pass
        # Wallets.re_charge_wallet(user_id, bank_name, amount)

    @classmethod
    def buy_subscription_func(cls, username, data_dict_command):
        pass
        # Subscriptions.buy_subscription(user_id, subs_type)

    @classmethod
    def add_bank_account_func(cls, username, data_dict_command):
        pass

    @classmethod
    def show_films_func(cls, username, data_dict_command):
        pass

    @classmethod
    def choose_film(cls, username, data_dict_command):
        pass

    @classmethod
    def show_screens_func(cls, username, data_dict_command):
        pass

    @classmethod
    def choose_screen_func(cls, username, data_dict_command):
        pass

    @classmethod
    def show_seats_func(cls, username, data_dict_command):
        pass

    @classmethod
    def choose_seat_func(cls, username, data_dict_command):
        pass

    @classmethod
    def cancel_reservation_func(cls, username, data_dict_command):
        pass

    @classmethod
    def show_watched_films_func(cls, username, data_dict_command):
        pass

    @classmethod
    def send_score_film_func(cls, username, data_dict_command):
        pass

    @classmethod
    def show_films_scores(cls, username, data_dict_command):
        pass

    @classmethod
    def show_comments_film_func(cls, username, data_dict_command):
        pass

    @classmethod
    def send_comment(cls, username, data_dict_command):
        pass

    @classmethod
    def reply_comment_func(cls, username, data_dict_command):
        pass

    @classmethod
    def send_message_to_support_func(cls, username, data_dict_command):
        pass

    @classmethod
    def auto_reservation_func(cls, username, data_dict_command):
        pass

    @classmethod
    def add_screens_func(cls, username, data_dict_command):
        pass

    @classmethod
    def send_message_employee(cls, username, data_dict_command):
        pass

    @classmethod
    def add_session(cls, username, data_dict_command):
        pass

    @classmethod
    def add_film(cls, username, data_dict_command):
        pass

    @classmethod
    def add_seats(cls, username, data_dict_command):
        pass


# Create instances of Interaction_Commands classes
interactions_commands_instance = InteractionsCommands()

interactions_commands = {
    'change_username': interactions_commands_instance.change_username_func,
    'change_password': interactions_commands_instance.change_password_func,
    'change_email': interactions_commands_instance.change_email_func,
    'change_phoneNumber': interactions_commands_instance.change_phoneNumber,
    'show_profile': interactions_commands_instance.show_profile_func,
    'add_screens': interactions_commands_instance.add_screens_func,
    'send_message_employee': interactions_commands_instance.send_message_employee,
    'add_session': interactions_commands_instance.add_session,
    'add_film': interactions_commands_instance.add_film,
    'add_seats': interactions_commands_instance.add_seats,
    'show_balance': interactions_commands_instance.show_balance_func,
    'show_bank_accounts': interactions_commands_instance.show_bank_accounts_func,
    'show_reservation': interactions_commands_instance.show_reservation_func,
    'show_subscription_detail': interactions_commands_instance.show_subscription_detail_func,
    'remove_account': interactions_commands_instance.remove_account_func,
    'add_bank_Account': interactions_commands_instance.add_bank_Account_func,
    're_charge': interactions_commands_instance.re_charge_func,
    'buy_subscription': interactions_commands_instance.buy_subscription_func,
    'add_bank_account': interactions_commands_instance.add_bank_account_func,
    'show_films': interactions_commands_instance.show_films_func,
    'choose_film': interactions_commands_instance.choose_film,
    'show_screens': interactions_commands_instance.show_screens_func,
    'choose_screen': interactions_commands_instance.choose_screen_func,
    'show_seats': interactions_commands_instance.show_seats_func,
    'choose_seat': interactions_commands_instance.choose_seat_func,
    'cancel_reservation': interactions_commands_instance.cancel_reservation_func,
    'show_watched_films': interactions_commands_instance.show_watched_films_func,
    'send_score_film': interactions_commands_instance.send_score_film_func,
    'show_films_scores': interactions_commands_instance.show_films_scores,
    'show_comments_film': interactions_commands_instance.show_comments_film_func,
    'send_comment': interactions_commands_instance.send_comment,
    'reply_comment': interactions_commands_instance.reply_comment_func,
    'send_message_to_support': interactions_commands_instance.send_message_to_support_func,
    'auto_reservation': interactions_commands_instance.auto_reservation_func,
}

# user_interactions_commands_instance.
# admin_interaction_commands_instance.show_admin_services()
# common_interactions_commands_instance.change_password_func("mohammad")
