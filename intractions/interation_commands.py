class Interaction_Command:
    @classmethod
    def change_username_func(cls):
        return "hi"

    @classmethod
    def change_password_func(cls):
        pass

    @classmethod
    def change_email_func(cls):
        pass

    @classmethod
    def change_phpneNumber(cls):
        pass

    @classmethod
    def remove_bank_account_func(cls):
        pass

    @classmethod
    def show_ballance_func(cls):
        pass

    @classmethod
    def show_bank_accounts_func(cls):
        pass

    @classmethod
    def show_reservation_func(cls):
        pass

    @classmethod
    def show_subscription_detail_func(cls):
        pass

    @classmethod
    def remove_account_func(cls):
        pass

    @classmethod
    def add_bank_Account_func(cls):
        pass

    @classmethod
    def re_charge_func(cls):
        pass

    @classmethod
    def buy_buy_subsctiption_func(cls):
        pass

    @classmethod
    def add_bank_account_func(cls):
        pass

    @classmethod
    def show_profile_func(cls):
        pass

    @classmethod
    def show_films_func(cls):
        pass

    @classmethod
    def chose_film(cls):
        pass

    @classmethod
    def show_screens_func(cls):
        pass

    @classmethod
    def choose_scren_func(cls):
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
    def add_screens_func(cls):
        pass

    @classmethod
    def show_watche_films_func(cls):
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
    def send_Message_employee(cls):
        pass

    @classmethod
    def send_message_to_support_func(cls):
        pass

    @classmethod
    def auto_reservation_func(cls):
        pass

# Create an instance of Interaction_Command
interaction_instance = Interaction_Command()

Interaction_Commands = {
    'change_username': interaction_instance.change_username_func,
    'change_password': interaction_instance.change_password_func,
    'change_email': interaction_instance.change_email_func,
    'change_phpneNumber': interaction_instance.change_phpneNumber,
    'remove_bank_account': interaction_instance.remove_bank_account_func,
    'show_ballance': interaction_instance.show_ballance_func,
    'show_bank_accounts': interaction_instance.show_bank_accounts_func,
    'show_reservation': interaction_instance.show_reservation_func,
    'show_subscription_detail': interaction_instance.show_subscription_detail_func,
    'remove_account': interaction_instance.remove_account_func,
    'add_bank_Account': interaction_instance.add_bank_Account_func,
    're_charge': interaction_instance.re_charge_func,
    'buy_subsctiption': interaction_instance.buy_buy_subsctiption_func,
    'add_banck_account': interaction_instance.add_bank_account_func,
    'show_profile': interaction_instance.show_profile_func,
    'show_films': interaction_instance.show_films_func,
    'chose_film': interaction_instance.chose_film,
    'show_screens': interaction_instance.show_screens_func,
    'choose_screen': interaction_instance.choose_scren_func,
    'show_seats': interaction_instance.show_seats_func,
    'choose_seat': interaction_instance.choose_seat_func,
    'cancel_reservation': interaction_instance.cancel_reservation_func,
    'add_screens': interaction_instance.add_screens_func,
    'show_watched_films': interaction_instance.show_watche_films_func,
    'send_score_film': interaction_instance.send_score_film_func,
    'show_films_scores': interaction_instance.show_films_scores,
    'show_comments_film': interaction_instance.show_comments_film_func,
    'send_comment': interaction_instance.send_comment,
    'reply_comment': interaction_instance.reply_comment_func,
    'send_Message_employee': interaction_instance.send_Message_employee,
    'send_message_to_support': interaction_instance.send_message_to_support_func,
    'auto_reservation': interaction_instance.auto_reservation_func
}

# Interaction_Commands['change_username']()
