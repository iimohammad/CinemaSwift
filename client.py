import socket
import json
import argparse
import getpass
from intractions import interation_commands
from settings import local_settings
from intractions import clear_screen
from datetime import datetime

class clientSettings:
    def __init__(self):
        self.is_admin = False

    def set_is_admin(self):
        self.is_admin = True

    def get_is_admin(self):
        return self.is_admin

class TCPClient:
    def __init__(
            self,
            host=local_settings.Network['host'],
            port=local_settings.Network['port']):
        self.host = host
        self.port = int(port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_dict_to_server(self, data_dict):
        try:
            json_string = json.dumps(data_dict)
            self.client_socket.sendall(json_string.encode('utf-8'))
            print(f"Sent dictionary to the server:\n{data_dict}")

            response = self.client_socket.recv(3072)
            # print(
            #     f"""Received response from the server: {
            #     response.decode('utf-8')}""")
            return response
        except ConnectionAbortedError:
            print("Connection to the server was unexpectedly closed.")
            raise  # Re-raise the exception to let the calling code handle it

        except Exception as e:
            print(f"An error occurred: {e}")
            return b''  # Return an empty byte string or han

    def close_connection(self):
        self.client_socket.close()
        print("Connection closed.")


def show_services():
    for key, value in interation_commands.interactions_commands.items():
        print(key)

def main():
    global send_data, comment, parent_id
    parser = argparse.ArgumentParser(
        description="Client for Movie Reservation System")
    parser.add_argument(
        'action',
        choices=[
            'signup',
            'login'],
        help='Specify the action to perform (signup or login)')
    parser.add_argument(
        '--username',
        help='Specify the username for signup or login')

    args = parser.parse_args()

    client = TCPClient()
    try:
        client.connect()

        if args.action == 'signup':
            if not args.username:
                print("Error: Username is required for signup.")
                return
            password = getpass.getpass("Enter password: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            birthday = input("Enter birthday: ")

            data_to_send = {
                'action': 'signup',
                'username': args.username,
                'password': password,
                'email': email,
                'phone': phone,
                'birthday': birthday
            }
            # response = client.send_dict_to_server(data_dict=data_to_send)
            # print(response)

        elif args.action == 'login':
            if not args.username:
                print("Error: Username is required for login.")
                return
            password = getpass.getpass("Enter password: ")
            data_to_send = {
                'action': 'login',
                'username': args.username,
                'password': password
            }

        else:
            print("Invalid action.")
            return

        response = client.send_dict_to_server(data_dict=data_to_send)
        local_client_settings = clientSettings()
        if response.decode('utf-8') == "Admin Login successful":
            local_client_settings.set_is_admin()

        if response.decode('utf-8') == "Login successful!" or response.decode('utf-8') == "Admin Login successful":
            while args.action == 'login':
                command = input(
                    "Enter a command or if you want to see all of our services enter show_services:\n ")
                if command.lower() == 'logout':
                    break
                else:
                    if command == "show_services":
                        command_to_send = {'action': command, }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "buy_ticket":
                        seat_id = input("Enter seat id : ")
                        command_to_send = {'action': command,
                                           'seat_id': seat_id}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "buy_subscription":
                        print("""subscriptions:
                              1- Gold: 50 percent discount with free drink for 1 month
                              2- Silver: 20 percent discount for 3 next buy""")
                        subscription_id  = input("please choose your subscription type : ")
                        command_to_send = {'action': command,
                                           'subscription_id': subscription_id}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "change_username":
                        send_data = input("Enter new username please:")
                        command_to_send = {'action': command,
                                           'username': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "change_password":
                        password = getpass.getpass("Enter new password:")
                        password_repeat = getpass.getpass("Enter new password again:")
                        if password != password_repeat:
                            print('password and repeat must be same!')
                            continue
                        command_to_send = {'action': command,
                                           'password': password}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "change_email":
                        send_data = input("Enter new email:")

                        command_to_send = {'action': command,
                                           'email': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "change_phoneNumber":
                        send_data = input("Enter new phone Number:")

                        command_to_send = {'action': command,
                                           'phoneNumber': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_profile":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "add_screens":
                        if local_client_settings.get_is_admin():
                            film_id = input("Enter film id:")
                            number_of_screens = int(input("Enter number_of_screens:"))
                            command_to_send = {'action': command,
                                               'film_id': film_id,
                                               'number_of_screens': number_of_screens
                                               }
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            print(login_response.decode('utf-8'))
                        else:
                            print("Access denied")
                    elif command == "show_sessions":
                        screen_id = int(input("Enter screen_id : "))
                        command_to_send = {'action': command,
                                           'screen_id' : screen_id}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "add_film":
                        if local_client_settings.get_is_admin():
                            film_name = input("Enter film name:")
                            age_rating = int(input("Enter age rating:"))
                            duration = int(input("Enter duration:"))
                            command_to_send = {'action': command,
                                               'name': film_name,
                                               'age_rating': age_rating,
                                               'duration': duration
                                               }
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            print(login_response.decode('utf-8'))
                        else:
                            print("Access denied")
                    elif command == "remove_film":
                        if local_client_settings.get_is_admin():
                            film_id = input("Enter film id:")
                            command_to_send = {'action': command,
                                               'film_id': film_id,
                                                }
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            print(login_response.decode('utf-8'))
                        else:
                            print("Access denied")
                    elif command == "add_session":
                        if local_client_settings.get_is_admin():
                            screen_id = input("Enter screen id:")
                            start_time = input("Enter start time(datetime-'%Y-%m-%d %H:%M'):")
                            capacity = int(input("Enter capacity:"))
                            ticket_price = int(input("Enter ticket price for this session:"))
                            command_to_send = {'action': command,
                                                'screen_id': screen_id,
                                               'start_time': start_time,
                                               'capacity': capacity,
                                               'ticket_price': ticket_price
                                               }
                            datetime_format = "%Y-%m-%d %H:%M"
                            try:
                                datetime.strptime(start_time, datetime_format)
                            except Exception:
                                print("wrong datetime format")
                                continue
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            print(login_response.decode('utf-8'))
                        else:
                            print("Access denied")

                    elif command == "send_message_employee":
                        if local_client_settings.get_is_admin():
                            pass
                        else:
                            print("Access denied")

                    elif command == "send_comment":
                        film_id = input("Enter film id : ")
                        new_or_reply = input("Enter you want to reply or new comment: 1 for new, 2 for reply")
                        if int(new_or_reply) == 1:
                            comment = input("Type your comment:")
                            parent_id = -1

                        elif int(new_or_reply) == 2:
                            parent_id = int(input("Enter the number of which comment you want to reply:"))
                            comment = input("Type your comment:")
                        else:
                            print("wrong choose")

                        command_to_send = {'action': command,
                                           'text': comment,
                                           'film_id': film_id,
                                           'parent_comments_id': parent_id
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_comments_film":
                        film_id = input("Enter film_id : ")
                        command_to_send = {'action': command,
                                           'film_id': film_id}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "send_point":
                        film_id = input("Enter film_id : ")
                        point = input("Enter point : ")
                        command_to_send = {'action': command,
                                           'film_id' : film_id,
                                           'point' : point,}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_watched_films":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "cancel_reservation":
                        send_data = input("Enter ticket_id")
                        command_to_send = {'action': command,
                                        'ticket_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_seats":
                        session_id = input("Enter session_id : ")
                        command_to_send = {'action': command,
                                           'session_id': session_id}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_screens":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_films":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "add_bank_account":
                        bank_account_name = input("Enter bank Account name : ")
                        cvv2 = input("Enter the CVV2 : ")
                        password = getpass.getpass("Enter the password : ")
                        command_to_send = {'action': command,
                                           'name': bank_account_name,
                                           'cvv': cvv2,
                                           'password': password
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "charge_wallet":
                        amount = int(input("How much do you want to charge : "))
                        account_name = input("Enter bank account name : ")
                        cvv = input("Enter bank account cvv : ")
                        password = getpass.getpass("Enter bank account password : ")
                        command_to_send = {'action': command,
                                           'amount': amount,
                                           'account_name':account_name,
                                           'cvv':cvv,
                                           'password':password,
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))
                    elif command == "charge_bank_account":
                        amount = int(input("How much do you want to charge : "))
                        account_name = input("Enter bank account name : ")
                        command_to_send = {'action': command,
                                           'amount': amount,
                                           'account_name':account_name,
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_reservations":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_bank_accounts":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    elif command == "show_wallet_balance":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

        elif response == "Incorrect Password":
            print("You Enter wrong Password ")
        else:
            print("Print Signup first")

    finally:
        client.close_connection()


if __name__ == "__main__":
    main()
