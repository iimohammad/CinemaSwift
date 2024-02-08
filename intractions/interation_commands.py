from db import models
from payment_module.bankaccounts import BankAccounts
from payment_module.wallet import Wallets
from reservation_module.tickets import Ticket
from users_module.users import Users, Subscriptions


class CommonInteractionsCommands:
    @classmethod
    def change_username_func(cls, username: str, new_username):
        if Users.change_username(username=username, new_username=new_username):
            response = "change successfully"
            return response

    @classmethod
    def change_password_func(cls, username: str, new_password):
        Users.change_password(username=username, password=new_password)

    @classmethod
    def change_email_func(cls, username, new_email):
        Users.change_email(username=username, email=new_email)

    @classmethod
    def change_phoneNumber(cls, username, new_phone):
        Users.change_phone_number(username=username, phone=new_phone)

    @classmethod
    def show_profile_func(cls, username=None):
        Users.show_profile(username=username)


class UserInteractionsCommands:
    @classmethod
    def show_user_services(cls):
        for key in common_interactions_commands.keys():
            print(key)
        for key in user_interactions_commands.keys():
            print(key)

    @classmethod
    def remove_bank_account_func(cls, name):
        BankAccounts.remove_bank_account(name)

    @classmethod
    def show_balance_func(cls, username):
        Wallets.get_balance_by_username(username)

    @classmethod
    def show_bank_accounts_func(cls, username=None):
        BankAccounts.show_all_accounts_by_username(username=username)

    @classmethod
    def show_reservation_func(cls, username=None):
        Ticket.show_all_buy_tickets(username=username)

    @classmethod
    def show_subscription_detail_func(cls, user_id):
        type_subs = Subscriptions.get_subscription_type_name(user_id)
        if type_subs == 3:
            print("options of this Golden subscription is:")
        elif type_subs == 2:
            print("options of this Silver subscription is:")
        else:
            print("options of this Bronze subscription is:")

    @classmethod
    def remove_account_func(cls, user_id):
        Users.remove_account(user_id)

    @classmethod
    def add_bank_Account_func(cls, account: models.bank_account_model):
        BankAccounts.add_bank_account(account)
        
    @classmethod
    def re_charge_func(cls, user_id=None, bank_name=None, amount=None):
        # descrese from banck account and increase the wallet
        Wallets.re_charge_wallet(user_id, bank_name, amount)

    @classmethod
    def buy_subscription_func(cls, user_id=None, subs_type=None):
        Subscriptions.buy_subscription(user_id, subs_type)

    @classmethod
    def add_bank_account_func(cls, user_id):
        pass

    @classmethod
    def show_films_func(cls):
        pass

    @classmethod
    def choose_film(cls):
        pass

    @classmethod
    def show_screens_func(cls):
        pass

    @classmethod
    def choose_screen_func(cls):
        pass

    @classmethod
    def show_seats_func(cls):
        pass

    @classmethod
    def choose_seat_func(cls):
        pass

    @classmethod
    def cancel_reservation_func(cls):
        pass

    @classmethod
    def show_watched_films_func(cls):
        pass

    @classmethod
    def send_score_film_func(cls):
        pass

    @classmethod
    def show_films_scores(cls):
        pass

    @classmethod
    def show_comments_film_func(cls):
        pass

    @classmethod
    def send_comment(cls):
        pass

    @classmethod
    def reply_comment_func(cls):
        pass

    @classmethod
    def send_message_to_support_func(cls):
        pass

    @classmethod
    def auto_reservation_func(cls):
        pass


class AdminInteractionCommands:
    @classmethod
    def show_admin_services(cls):
        keys_with_newlines = '\n'.join(common_interactions_commands.keys() + admin_interaction_commands.keys())
        return keys_with_newlines

    @classmethod
    def add_screens_func(cls):
        pass

    @classmethod
    def send_message_employee(cls):
        pass

    @classmethod
    def add_session(cls):
        pass

    @classmethod
    def add_film(cls):
        pass

    @classmethod
    def add_seats(cls):
        pass

    @classmethod
    def remove_film(cls):
        pass


# Create instances of Interaction_Commands classes
admin_interaction_commands_instance = AdminInteractionCommands()
user_interactions_commands_instance = UserInteractionsCommands()
common_interactions_commands_instance = CommonInteractionsCommands()

# Define dictionaries for command mapping
admin_interaction_commands = {
    'show_admin_services': admin_interaction_commands_instance.show_admin_services,
    'add_screens': admin_interaction_commands_instance.add_screens_func,
    'send_message_employee': admin_interaction_commands_instance.send_message_employee,
    'add_session': admin_interaction_commands_instance.add_session,
    'add_film': admin_interaction_commands_instance.add_film,
    'add_seats': admin_interaction_commands_instance.add_seats,
    'remove_film': admin_interaction_commands_instance.remove_film,
}

user_interactions_commands = {
    'remove_bank_account': user_interactions_commands_instance.remove_bank_account_func,
    'show_balance': user_interactions_commands_instance.show_balance_func,
    'show_bank_accounts': user_interactions_commands_instance.show_bank_accounts_func,
    'show_reservation': user_interactions_commands_instance.show_reservation_func,
    'show_subscription_detail': user_interactions_commands_instance.show_subscription_detail_func,
    'remove_account': user_interactions_commands_instance.remove_account_func,
    'add_bank_Account': user_interactions_commands_instance.add_bank_Account_func,
    're_charge': user_interactions_commands_instance.re_charge_func,
    'buy_subscription': user_interactions_commands_instance.buy_subscription_func,
    'add_bank_account': user_interactions_commands_instance.add_bank_account_func,
    'show_films': user_interactions_commands_instance.show_films_func,
    'choose_film': user_interactions_commands_instance.choose_film,
    'show_screens': user_interactions_commands_instance.show_screens_func,
    'choose_screen': user_interactions_commands_instance.choose_screen_func,
    'show_seats': user_interactions_commands_instance.show_seats_func,
    'choose_seat': user_interactions_commands_instance.choose_seat_func,
    'cancel_reservation': user_interactions_commands_instance.cancel_reservation_func,
    'show_watched_films': user_interactions_commands_instance.show_watched_films_func,
    'send_score_film': user_interactions_commands_instance.send_score_film_func,
    'show_films_scores': user_interactions_commands_instance.show_films_scores,
    'show_comments_film': user_interactions_commands_instance.show_comments_film_func,
    'send_comment': user_interactions_commands_instance.send_comment,
    'reply_comment': user_interactions_commands_instance.reply_comment_func,
    'send_message_to_support': user_interactions_commands_instance.send_message_to_support_func,
    'auto_reservation': user_interactions_commands_instance.auto_reservation_func,
}

common_interactions_commands = {
    'change_username': common_interactions_commands_instance.change_username_func,
    'change_password': common_interactions_commands_instance.change_password_func,
    'change_email': common_interactions_commands_instance.change_email_func,
    'change_phoneNumber': common_interactions_commands_instance.change_phoneNumber,
    'show_profile': common_interactions_commands_instance.show_profile_func
}

# user_interactions_commands_instance.
# admin_interaction_commands_instance.show_admin_services()
# common_interactions_commands_instance.change_password_func("mohammad")
