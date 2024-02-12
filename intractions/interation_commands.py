from db import models
from payment_module.bankaccounts import BankAccounts
from payment_module.wallet import Wallets
from reservation_module.tickets import Ticket
from users_module.users import Users, Subscriptions
from comments_module.films import Films , FilmsPoints
from comments_module.films import Films , FilmsPoints , Comments
from screen_module.screens import Screens,Session,Seats

class InteractionsCommands:
    @classmethod
    def change_username_func(cls, user_id: str, data_dict_command):
        new_username = data_dict_command['username']
        
        try:
            Users.change_username(user_id=user_id, new_username=new_username)
            return "change username successfully"
        except Exception as e:
            return e

    @classmethod
    def change_password_func(cls, user_id: str, data_dict_command):
        new_password = data_dict_command['password']
        try:
            Users.change_password(user_id=user_id, password=new_password)
            response = "change password successfully"
            return response
        except Exception as e:
            return e

    @classmethod
    def change_email_func(cls, user_id, data_dict_command):
        new_email = data_dict_command['email']
        try:
            Users.change_user_email(user_id=user_id, email=new_email)
            response = "change Email successfully"
            return response
        except Exception as e:
            return e

    @classmethod
    def change_phoneNumber(cls, user_id:str, data_dict_command):
        new_phone = data_dict_command['phoneNumber']
        try:
            Users.change_user_phone(user_id=user_id, phone=new_phone)
            response = "change phone Number successfully"
            return response
        except Exception as e:
            return e

    @classmethod
    def show_profile_func(cls, user_id):
        return Users.show_profile(user_id=user_id)

    # @classmethod
    # def remove_bank_account_func(cls, user_id,data_dict_command):
    #     # BankAccounts.remove_bank_account(name)
    #     pass

    @classmethod
    def show_wallet_balance_func(cls, user_id):
        try:
            return Wallets.get_balance(user_id)
        except Exception as e:
            return e
    
    @classmethod
    def show_bank_account_balance_func(cls, user_id,data_dict_command):
        account_name = data_dict_command['account_name']
        password_account = data_dict_command['password_account']
        cvv = data_dict_command['cvv']
        try:
            return BankAccounts.get_bank_account_balance(user_id ,account_name,cvv,password_account)
        except Exception as e:
            return e

    @classmethod
    def show_bank_accounts_func(cls, user_id):
        try:
            return BankAccounts.get_bank_accounts(user_id=user_id)
        except Exception as e:
            return e

    @classmethod
    def show_reservation_func(cls, user_id):
        # 
        pass

    # @classmethod
    # def show_subscription_detail_func(cls, user_id,data_dict_command):
    #     # type_subs = Subscriptions.get_subscription_type_name(user_id)
    #     # if type_subs == 3:
    #     #     print("options of this Golden subscription is:")
    #     # elif type_subs == 2:
    #     #     print("options of this Silver subscription is:")
    #     # else:
    #     #     print("options of this Bronze subscription is:")
    #     pass
    # @classmethod
    # def remove_account_func(cls, user_id,data_dict_command):
    #     # Users.remove_account(user_id)
    #     pass

    @classmethod
    def add_bank_Account_func(cls, user_id,data_dict_command):
        name = data_dict_command['name']
        cvv = data_dict_command['cvv']
        password = data_dict_command['password']
        try:
            BankAccounts.add_bank_account(
            models.bank_account_model(-1,user_id,name,0,cvv,password)
            )
            return True
        except Exception as e:
            return e
    @classmethod
    def re_charge_func(cls, user_id,data_dict_command):
        amount = data_dict_command['amount']
        try:
            return Wallets.deposit_to_wallet(user_id, amount)
        except Exception as e:
            return e
    @classmethod
    def buy_subscription_func(cls, username,data_dict_command):
        # Subscriptions.buy_subscription(user_id, subs_type)
        pass
    @classmethod
    def add_wallet_func(cls, user_id):
        try:
            Wallets.create_wallet(user_id)
        except Exception as e:
            return e

    @classmethod
    def show_films_func(cls):
        return Films.get_films_list()

    @classmethod
    def choose_film(cls,data_dict_command):
        film_id = data_dict_command['film_id']
        try:
            return Films.get_film(film_id=film_id)
        except Exception as e:
            return e

    @classmethod
    def show_screens_func(cls):
        return Screens.get_screens_list()
    
    @classmethod
    def show_sessions_available_func(cls,data_dict_command):
        screen_id = data_dict_command['screen_id']
        return Session.get_available_sessions(screen_id=screen_id)

    @classmethod
    def show_seats_func(cls,data_dict_command):
        session_id = data_dict_command['session_id']
        return Seats.get_seats_of_a_session(session_id=session_id)

    @classmethod
    def cancel_reservation_func(cls,data_dict_command):
        ticket_id = data_dict_command['ticket_id']
        try:
            Ticket.cancel_ticket(ticket_id=ticket_id)
        except Exception as e:
            return e

    @classmethod
    def show_all_tickets_of_user(cls,user_id):
        return Ticket.show_all_tickets_by_user(user_id=user_id)

    @classmethod
    def show_watched_films_func(cls,user_id):
        return Ticket.show_all_past_tickets_by_user(user_id)

    @classmethod
    def send_score_film_func(cls,user_id,data_dict_command):
        film_id = data_dict_command['film_id']
        point = data_dict_command['point']
        FilmsPoints.add_point(user_id,film_id,point)
        return True

    @classmethod
    def show_films_scores(cls):
        return Films.get_films_list()

    @classmethod
    def show_comments_film_func(cls,data_dict_command):
        film_id = data_dict_command['film_id']
        return Comments.get_comments_of_film(film_id)

    @classmethod
    def send_comment(cls,user_id,data_dict_command):
        film_id = data_dict_command['film_id']
        text = data_dict_command['text']
        parent_comments_id = data_dict_command['parent_comments_id']
        Comments.add_comment(models.comment_model(-1,film_id,user_id,text,parent_comments_id,''))
        return True

    @classmethod
    def send_message_to_support_func(cls,username,data_dict_command):
        pass

    # @classmethod
    # def auto_reservation_func(cls,username,data_dict_command):
    #     pass

    @classmethod
    def add_screens_func(cls,data_dict_command):
        film_id = data_dict_command['film_id']
        number_of_screens = data_dict_command['number_of_screens']
        try:
            Screens.create_screen(models.screen_model(-1,film_id,number_of_screens))
            return True
        except Exception as e:
            return e

    @classmethod
    def send_message_employee(cls,username,data_dict_command):
        pass

    @classmethod
    def add_session(cls,data_dict_command):
        screen_id = data_dict_command['screen_id']
        start_time = data_dict_command['start_time']
        capacity = data_dict_command['capacity']
        ticket_price = data_dict_command['ticket_price']
        try:
            Session.create_session(models.session_model(-1,screen_id,start_time,capacity,ticket_price))
        except Exception as e:
            return e

    @classmethod
    def add_film(cls,data_dict_command):
        name = data_dict_command['name']
        age_rating = data_dict_command['age_rating']
        duration = data_dict_command['duration']
        Films.add_film(models.film_model(-1,name,age_rating,duration,0))
        return True

    @classmethod
    def remove_film(cls,data_dict_command):
        film_id = data_dict_command['film_id']
        try:
            Films.remove_film(film_id)
        except Exception as e:
            return e
    
    @classmethod
    def chat_func(cls, logged_in_admins, client_socket, data_dict_command):
        logged_in_admins.pop(client_socket)

        if data_dict_command['status'] == "Send online admins' list":
            return logged_in_admins
        elif data_dict_command['status'] == "Admin chosen":
            data_to_send = {'action': 'chat',
                            'status': "Chat request",
                            'admin_id': client_socket,
                            'message': "Pending request"}
            return data_to_send
        elif data_dict_command['status'] == "Chat acceptance":
            data_to_send = {'action': 'chat',
                            'status': "Chatting",
                            'admin_id': data_dict_command['admin_id'],
                            'message': data_dict_command['message']}
            return data_to_send
        elif data_dict_command['status'] == "Chatting":
            data_to_send = {'action': 'chat',
                            'status': "Chatting",
                            'admin_id': data_dict_command['admin_id'],
                            'message': data_dict_command['message']}
            return data_to_send


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
    'remove_film': interactions_commands_instance.remove_film,
    'remove_bank_account': interactions_commands_instance.remove_bank_account_func,
    'show_balance': interactions_commands_instance.show_wallet_balance_func,
    'show_bank_accounts': interactions_commands_instance.show_bank_accounts_func,
    'show_reservation': interactions_commands_instance.show_reservation_func,
    'show_subscription_detail': interactions_commands_instance.show_subscription_detail_func,
    'remove_account': interactions_commands_instance.remove_account_func,
    'add_bank_Account': interactions_commands_instance.add_bank_Account_func,
    're_charge': interactions_commands_instance.re_charge_func,
    'buy_subscription': interactions_commands_instance.buy_subscription_func,
    'add_bank_account': interactions_commands_instance.add_bank_Account_func,
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
    'chat': interactions_commands_instance.chat_func,
}

# user_interactions_commands_instance.
# admin_interaction_commands_instance.show_admin_services()
# common_interactions_commands_instance.change_password_func("mohammad")
