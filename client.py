import socket
import json
import argparse
import getpass
import time
import threading
from intractions import interation_commands
from settings import local_settings
from intractions import clear_screen


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

            response = self.client_socket.recv(1024)
            print(
                f"Received response from the server: {response.decode('utf-8')}")
            try:
                response = json.loads(response)
            except:
                pass
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

def send_input(admin_username, admin_socket, my_socket):
    while True:
        try:
            chat_message = input()
            if chat_message == '> exit':
                command_to_send = {'action': 'chat',
                                   'status': "Chat ended",
                                   'admin_username': admin_username}
                json_string = json.dumps(command_to_send)
                my_socket.sendall(json_string.encode('utf-8'))
                print("Chat ended")
                break
            command_to_send = {'action': 'chat',
                               'status': "Chatting",
                               'admin_username': admin_username,
                               'message': chat_message}
            json_string = json.dumps(command_to_send)
            my_socket.sendall(json_string.encode('utf-8'))
        except KeyboardInterrupt:
            command_to_send = {'action': 'chat',
                               'status': "Chat ended",
                               'admin_username': admin_username}
            json_string = json.dumps(command_to_send)
            my_socket.sendall(json_string.encode('utf-8'))
            print("Chat ended")
            break
        except ConnectionAbortedError:
            print("Connection to the server was unexpectedly closed.")
            print("Chat ended")
            raise
            break

def get_message(admin_username, admin_socket, my_socket):
    while True:
        try:
            response = my_socket.recv(1024)
            response = json.loads(response)
            if response['action'] == 'chat' and response['status'] == 'Chatting':
                print(f" >> {admin_username}'s message: {response['message']}")
            elif response['action'] == 'chat' and response['status'] == 'Chat ended':
                print(f"Chat ended by {admin_username}! Please type '> exit' or press Ctrl+C to exit chat")
                break
        except KeyboardInterrupt:
            command_to_send = {'action': 'chat',
                               'status': "Chat ended",
                               'admin_username': admin_username}
            json_string = json.dumps(command_to_send)
            my_socket.sendall(json_string.encode('utf-8'))
            print("Chat ended")
            break
        except ConnectionAbortedError:
            print("Connection to the server was unexpectedly closed.")
            print("Chat ended")
            raise
            break

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
                    command_to_send = {'action': command}
                    login_response = client.send_dict_to_server(
                        data_dict=command_to_send)
                    break
                else:
                    if command == "check_chat_requests":

                        # Here is where the problem begins!
                        # This method is not able to get chat requests!
                        # It's because the typical client-server tcp channel we use
                        # is unable to handle a connection between two clients
                        data = client.client_socket.recv(1024)
                        try:
                            response = json.loads(data)
                        except:
                            response = data.decode('utf-8')

                        if str(type(response)) == "<class 'str'>":
                            print("No chat requests received")
                        elif response.get('status', 'None') == 'Chat request' \
                                    and response.get('action', 'None') == 'chat':
                            admin_username = response['admin_username']
                            admin_socket = response['admin_socket']
                            chat_acceptance = input(f"Do you want to chat with {admin_username}? (N/y)")

                            if chat_acceptance == "y":
                                print("The chat has begun! (to exit the chat, enter '> exit')")
                                command_to_send = {'action': 'chat',
                                                   'status': "Chat acceptance",
                                                   'admin_username': admin_username,
                                                   'message': 'Chat request accepted'}
                                json_string = json.dumps(command_to_send)
                                client.client_socket.sendall(json_string.encode('utf-8'))

                                thread1 = threading.Thread(target=send_input, \
                                                           args=(admin_username, admin_socket, client.client_socket))
                                thread2 = threading.Thread(target=get_message, \
                                                           args=(admin_username, admin_socket, client.client_socket))
                                thread1.start()
                                thread2.start()

                                thread1.join()
                                thread2.join()

                            elif chat_acceptance == "N":
                                client.client_socket.sendall(b'Chat request rejected')
                            else:
                                print("You entered the wrong command! Try again.")

                    if command == "chat":
                        chat_started = False
                        
                        command_to_send = {'action': command,
                                           'status': "Send online admins' list"}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)

                        counter = 0
                        for username in login_response:
                            counter += 1
                            print(f"{counter} - {username}")
                            print(" ")
                        
                        print("-------------------------------------")
                        admin_username = input("Enter the admin username you want to chat with:")
                        available = False
                        for username in login_response:
                            if username == admin_username:
                                available = True
                                break

                        waiting_needed = True
                        if available:
                            command_to_send = {'action': command,
                                               'status': "Admin chosen",
                                               'admin_username': admin_username}
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            if login_response.get('message', 'None') == "Chat request accepted":
                                print(f"{login_response['message']} (to exit chat, enter '> exit')")
                                chat_started = True
                                waiting_needed = False
                        else:
                            print("Wrong admin id entered! Try again.")
                            waiting_needed = False

                        while waiting_needed:
                            time.sleep(5)

                            # Even sending requests like what's happening here
                            # is unable to establish a connection between the two clients
                            # It's reason is the client-server channel is not designed
                            # so that two clients can communicate through it
                            command_to_send = {'action': command,
                                               'status': "Admin chosen",
                                               'admin_username': admin_username}
                            response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            try:
                                response = response.decode('utf-8')
                            except:
                                pass

                            if str(type(response)) == "<class 'str'>":
                                if response == 'Chat request rejected':
                                    print(f"{admin_username} rejected you chat request.")
                                    waiting_needed = False
                                desicion = input('Do you want to wait another 5 seconds \
                                                  for the chat acceptance? (N/y)')
                                if desicion == 'y':
                                    pass
                                elif desicion == 'N':
                                    print('Chat ended')
                                    waiting_needed = False
                                else:
                                    print("You entered the wrong command! Try again after 5 seconds.")
                            elif response.get('message', 'None') == "Chat request accepted":
                                print(f"{response['message']} (to exit chat, enter '> exit')")
                                chat_started = True
                                waiting_needed = False

                        if chat_started:
                            thread1 = threading.Thread(target=send_input, \
                                                       args=(admin_username, admin_socket, client.client_socket))
                            thread2 = threading.Thread(target=get_message, \
                                                       args=(admin_username, admin_socket, client.client_socket))
                            thread1.start()
                            thread2.start()

                            thread1.join()
                            thread2.join()
                            
                    if command == "show_services":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "change_username":
                        send_data = input("Enter new username please:")
                        command_to_send = {'action': command,
                                           'username': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "change_password":
                        send_data = getpass.getpass("Enter new password:")

                        command_to_send = {'action': command,
                                           'password': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "change_email":
                        send_data = input("Enter new email:")

                        command_to_send = {'action': command,
                                           'email': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "change_phoneNumber":
                        send_data = input("Enter new phone Number:")

                        command_to_send = {'action': command,
                                           'phoneNumber': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_profile":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "add_screens":
                        if local_client_settings.get_is_admin():
                            pass
                        else:
                            print("Access denied")

                    if command == "add_seats":
                        if local_client_settings.get_is_admin():
                            pass
                        else:
                            print("Access denied")

                    if command == "add_film":
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

                    if command == "add_session":
                        if local_client_settings.get_is_admin():
                            pass
                        else:
                            print("Access denied")

                    if command == "send_message_employee":
                        if local_client_settings.get_is_admin():
                            pass
                        else:
                            print("Access denied")

                    if command == "send_comment":
                        film_name = input("Enter the name of film")
                        new_or_reply = input("Enter you want to reply or new comment: 1: for new, 2 for reply")
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
                                           'film_name': film_name,
                                           'parent_comments_id': parent_id
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_comments_film":
                        send_data = input("Enter film_id")
                        command_to_send = {'action': command,
                                           'film_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_films_scores":
                        send_data = input("Enter film_id")
                        command_to_send = {'action': command,
                                           'film_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "send_score_film":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_watched_films":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "cancel_reservation":
                        send_data = input("Enter ticket_id")
                        command_to_send = {'action': command,
                                        'ticket_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_seats":
                        send_data = input("Enter session_id")
                        command_to_send = {'action': command,
                                           'session_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_screens":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "choose_film":
                        send_data = input("Enter film_id")
                        command_to_send = {'action': command,
                                           'film_id': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_films":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "add_bank_account":
                        bank_account_name = input("Enter bank Account name")
                        cvv2 = input("Enter the CVV2")
                        password = getpass.getpass("Enter the password")
                        command_to_send = {'action': command,
                                           'name': bank_account_name,
                                           'cvv': cvv2,
                                           'password': password
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "re_charge":
                        amount = int(input("How much do you want to charge"))
                        command_to_send = {'action': command,
                                           'amount': amount
                                           }
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_reservation":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_bank_accounts":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "show_balance":
                        command_to_send = {'action': command}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

        elif response == "Incorrect Password":
            print("You entered the wrong password ")
        else:
            print("Print signup first")

    finally:
        client.close_connection()


if __name__ == "__main__":
    main()
