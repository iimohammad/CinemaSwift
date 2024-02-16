from db import models
from payment_module.bankaccounts import BankAccounts
from payment_module.wallet import Wallets
from reservation_module.tickets import Ticket
from users_module.users import Users, Subscriptions
from comments_module.films import Films, FilmsPoints, Comments
from screen_module.screens import Screens, Session, Seats


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
    def change_phoneNumber(cls, user_id: str, data_dict_command):
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

    @classmethod
    def show_wallet_balance_func(cls, user_id):
        try:
            return Wallets.get_balance(user_id)
        except Exception as e:
            return e

    @classmethod
    def show_bank_account_balance_func(cls, user_id, data_dict_command):
        account_name = data_dict_command['account_name']
        password_account = data_dict_command['password_account']
        cvv = data_dict_command['cvv']
        try:
            return BankAccounts.get_bank_account_balance(user_id, account_name, cvv, password_account)
        except Exception as e:
            return e

    @classmethod
    def show_bank_accounts_func(cls, user_id, data_dict_command):
        try:
            resault_list = BankAccounts.get_bank_accounts(user_id=user_id)
            print(resault_list)
            r = ''
            for i in resault_list:
                r+=f"bank account name : {i[0]} - bank account balance : {i[1]}\n"
            return r
        except Exception as e:
            return e

    @classmethod
    def show_reservations_func(cls, user_id, data_dict_command):
        resault_list = Ticket.show_all_tickets_by_user(user_id)
        r = ''
        for i in resault_list:
            r+=f"""tickets id : {i[0]} - film name : {i[1]} - View date : {i[2]} _ seat number : {i[3]}\n"""
        return r

    @classmethod
    def add_bank_Account_func(cls, user_id, data_dict_command):
        name = data_dict_command['name']
        cvv = data_dict_command['cvv']
        password = data_dict_command['password']
        try:
            BankAccounts.add_bank_account(
                models.bank_account_model(-1, user_id, name, 0, cvv, password)
            )
            return True
        except Exception as e:
            return e

    @classmethod
    def charge_wallet_func(cls, user_id, data_dict_command):
        account_name = data_dict_command['account_name']
        amount = data_dict_command['amount']
        cvv = data_dict_command['cvv']
        password = data_dict_command['password']
        try:
            if BankAccounts.harvest_from_bank_account(user_id,cvv,password,amount,account_name):
                return Wallets.deposit_to_wallet(user_id, amount)
            return False
        except Exception as e:
            return e

    @classmethod
    def charge_bank_account_func(cls, user_id, data_dict_command):
        account_name = data_dict_command['account_name']
        amount = data_dict_command['amount']
        try:
            return BankAccounts.deposit_to_bank_account(user_id,account_name,amount)
        except Exception as e:
            return e
        
    @classmethod
    def buy_subscription_func(cls, user_id, data_dict_command):
        # Subscriptions.buy_subscription(user_id, subs_type)
        pass
    @classmethod
    def buy_ticket_func(cls, user_id, data_dict_command):
        try:
            seat_id = data_dict_command['seat_id']
            return Ticket.buy_ticket(user_id,seat_id)
        except Exception as e:
            return e
    @classmethod
    def add_wallet_func(cls, user_id, data_dict_command):
        try:
            Wallets.create_wallet(user_id)
        except Exception as e:
            return e

    @classmethod
    def show_films_func(cls, user_id, data_dict_command):

        response = ""
        films_list = Films.get_films_list()
        for item in films_list:
            id = item.id
            name = item.name
            age_rating = item.age_rating
            duration = item.duration
            point = item.point
            weighted_point = item.weighted_point
            response_item = f"id : {id} _ film name :{name} - age rating : {age_rating} - duration :{duration} - point:{point} -weighted_point: {weighted_point}"
            response += (response_item + "\n")
        return response

    @classmethod
    def show_screens_func(cls, user_id, data_dict_command):
        response = ""
        for item in Screens.get_screens_list():
            screen_id = item[0]
            film_name = item[1]
            number_of_sans = item[2]
            response += f"screen_id = {screen_id} - film_name = {film_name} -number_of_sans= {number_of_sans} \n"
        print(response)
        return response

    @classmethod
    def show_sessions_available_func(cls,user_id, data_dict_command):
        screen_id = data_dict_command['screen_id']
        result = Session.get_available_sessions(screen_id=screen_id)
        response = ""
        for item in result:
            session_id = item[0]
            film_name = item[1]
            start_time = item[2]
            ticket_price = item[3]
            response += f"session_id : {session_id} _ film_name : {film_name} - start_time : {start_time} - ticket_price : {ticket_price}\n"
        return response

    @classmethod
    def show_seats_func(cls,user_id, data_dict_command):
        session_id = data_dict_command['session_id']
        result_list = Seats.get_seats_of_a_session(session_id=session_id)
        response = ""
        for item in result_list:
            seat_id = item[0]
            seat_number = item[1]
            status = item[2]
            response += f"seat_id = {seat_id} - seat_number = {seat_number} - status = {status}\n"
        print(response)
        return response

    @classmethod
    def cancel_reservation_func(cls, data_dict_command):
        ticket_id = data_dict_command['ticket_id']
        try:
            Ticket.cancel_ticket(ticket_id=ticket_id)
        except Exception as e:
            return e

    @classmethod
    def show_all_tickets_of_user(cls, user_id, data_dict_command):

        resault_list = Ticket.show_all_tickets_by_user(user_id=user_id)
        r = ''
        for i in resault_list:
            r+=f"""tickets id : {i[0]} - film name : {i[1]} - View date : {i[2]} _ seat number : {i[3]}\n"""
        return r

    @classmethod
    def show_watched_films_func(cls, user_id, data_dict_command):
        resault_list = Ticket.show_all_past_tickets_by_user(user_id)
        r = ''
        for i in resault_list:
            r+=f"""tickets id : {i[0]} - film name : {i[1]} - View date : {i[2]} _ seat number : {i[3]}\n"""
        return r
    @classmethod
    def send_point_func(cls, user_id, data_dict_command):
        film_id = data_dict_command['film_id']
        point = data_dict_command['point']
        FilmsPoints.add_point(user_id, film_id, point)
        return True

    @classmethod
    def show_comments_film_func(cls, user_id, data_dict_command):
        film_id = data_dict_command['film_id']
        res = ''
        comment_list = Comments.get_comments_of_film(film_id)
        
        for i in comment_list:
            user_name = i[0]
            text = i[2]
            comment_id = i[1]
            created_at = i[3]
            reply_to = i[4]
            res += f"""comment id : {comment_id} 
            user name : {user_name}
            created at : {created_at} 
            reply to : {reply_to}
            text : {text}\n"""
        return res
    @classmethod
    def send_comment(cls, user_id, data_dict_command):
        film_id = data_dict_command['film_id']
        text = data_dict_command['text']
        parent_comments_id = data_dict_command['parent_comments_id']
        Comments.add_comment(models.comment_model(-1, film_id, user_id, text, parent_comments_id, ''))
        return True

    @classmethod
    def send_message_to_support_func(cls, user_id, data_dict_command):
        pass

    @classmethod
    def show_services(cls, user_id, data_dict_command):
        responselist = list()
        for i in interactions_commands:
            responselist.append(i)
        # print(responselist)
        response = ""
        if Users.is_admin(user_id=user_id):
            for i in responselist:
                response += (i + "\n")
        else:
            for i in range(min(23, len(responselist))):
                response += (responselist[i] + "\n")
        print(response)
        return response

    @classmethod
    def add_screens_func(cls, user_id, data_dict_command):
        film_id = data_dict_command['film_id']
        number_of_screens = data_dict_command['number_of_screens']
        try:
            # film_id = Films.get_filmid_by_name(film_name)
            Screens.create_screen(models.screen_model(-1, film_id, number_of_screens))
            return True
        except Exception as e:
            return e

    @classmethod
    def send_message_employee(cls, username, data_dict_command):
        pass

    @classmethod
    def add_session(cls, user_id, data_dict_command):
        screen_id = data_dict_command['screen_id']
        start_time = data_dict_command['start_time']
        capacity = data_dict_command['capacity']
        ticket_price = data_dict_command['ticket_price']
        try:
            return Session.create_session(models.session_model(-1, screen_id, start_time, capacity, ticket_price))
             
        except Exception as e:
            return e

    @classmethod
    def add_film(cls, user_id, data_dict_command):
        name = data_dict_command['name']
        age_rating = data_dict_command['age_rating']
        duration = data_dict_command['duration']
        Films.add_film(models.film_model(-1, name, age_rating, duration, 0, 0))
        return True

    @classmethod
    def remove_film(cls, user_id, data_dict_command):
        film_id = data_dict_command['film_id']
        try:
            Films.remove_film(film_id)
            return True
        except Exception as e:
            return e


# Create instances of Interaction_Commands classes
interactions_commands_instance = InteractionsCommands()

interactions_commands = {
    'add_bank_account': interactions_commands_instance.add_bank_Account_func,
    'add_session': interactions_commands_instance.add_session,
    'add_film': interactions_commands_instance.add_film,
    'add_screens': interactions_commands_instance.add_screens_func,
    'buy_subscription': interactions_commands_instance.buy_subscription_func,
    'buy_ticket': interactions_commands_instance.buy_ticket_func,
    'cancel_reservation': interactions_commands_instance.cancel_reservation_func,
    'change_email': interactions_commands_instance.change_email_func,
    'change_username': interactions_commands_instance.change_username_func,
    'change_password': interactions_commands_instance.change_password_func,
    'change_phoneNumber': interactions_commands_instance.change_phoneNumber,
    'show_profile': interactions_commands_instance.show_profile_func,
    'show_wallet_balance': interactions_commands_instance.show_wallet_balance_func,
    'show_bank_accounts': interactions_commands_instance.show_bank_accounts_func,
    'show_reservations': interactions_commands_instance.show_reservations_func,
    'show_screens': interactions_commands_instance.show_screens_func,
    'show_seats': interactions_commands_instance.show_seats_func,
    'show_films': interactions_commands_instance.show_films_func,
    'show_watched_films': interactions_commands_instance.show_watched_films_func,
    'show_comments_film': interactions_commands_instance.show_comments_film_func,
    'show_services': interactions_commands_instance.show_services,
    'show_sessions':interactions_commands_instance.show_sessions_available_func,
    'charge_wallet': interactions_commands_instance.charge_wallet_func,
    'charge_bank_account': interactions_commands_instance.charge_bank_account_func,
    'send_point': interactions_commands_instance.send_point_func,
    'send_comment': interactions_commands_instance.send_comment,
    'send_message_to_support': interactions_commands_instance.send_message_to_support_func,
    'send_message_employee': interactions_commands_instance.send_message_employee,
    'remove_film': interactions_commands_instance.remove_film,
}

# user_interactions_commands_instance.
# admin_interaction_commands_instance.show_admin_services()
# common_interactions_commands_instance.change_password_func("mohammad")
# interactions_commands_instance.show_films_func()
