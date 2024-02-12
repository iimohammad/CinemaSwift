import socket
import json
import argparse
import getpass
import time
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
                f"Received response from the server: {
                response.decode('utf-8')}")
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
    for key, value in interation_commands.Interaction_Commands.items():
        print(key)


def main():
    global send_data
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
                    "Enter a command or if you want to see all of our services enter -show services:\n ")
                if command.lower() == 'logout':
                    break
                else:
                    if command == "check_chat_requests":
                        data = client.client_socket.recv(1024)
                        response = data.decode('utf-8')

                        if response.get('status', 'None') == 'Chat request':
                            admin_id = response['admin_id']
                            chat_acceptance = input(f"Do you want to chat with {admin_id}? (N/y)")

                            if chat_acceptance == "y":
                                print("The chat has begun! (to exit the chat, enter '> exit')")
                                command_to_send = {'action': 'chat',
                                                   'status': "Chat acceptance",
                                                   'admin_id': admin_id,
                                                   'message': 'Chat request accepted'}
                                login_response = client.send_dict_to_server(
                                    data_dict=command_to_send)
                                login_response = login_response.decode('utf-8')
                                print(f"{admin_id}'s message: {login_response}")

                                while True:
                                    chat_message = input("Your message:")
                                    if chat_message == '> exit':
                                        print("Chat ended")
                                        break
                                    command_to_send = {'action': 'chat',
                                                    'status': "Chatting",
                                                    'admin_id': admin_id,
                                                    'message': chat_message}
                                    login_response = client.send_dict_to_server(
                                        data_dict=command_to_send)
                                    login_response = login_response.decode('utf-8')
                                    print(f"{admin_id}'s message: {login_response}")
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
                        admins_dict = login_response.decode('utf-8')
                        for admin_socket, admin_username in admins_dict.items():
                            print(f"{admin_socket}: {admin_username}")
                        
                        print("-------------------------------------")
                        admin_id = input("Enter the admin id you want to chat with:")
                        available = False
                        for admin_socket, admin_username in admins_dict.items():
                            if str(admin_socket) == admin_id:
                                available = True
                                admin_id = admin_socket
                                break
                        if available:
                            command_to_send = {'action': command,
                                            'status': "Admin chosen",
                                            'admin_id': admin_id}
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            login_response = login_response.decode('utf-8')
                            print(f"{login_response['message']}")
                        else:
                            print("Wrong admin id entered! Try again.")

                        while True:
                            time.sleep(5)
                            data = client.client_socket.recv(1024)
                            response = data.decode('utf-8')
                            if response['message'] == "Chat request accepted":
                                print(f"{response['message']} (to exit the chat, enter '> exit')")
                                chat_started = True
                                break
                            else:
                                desicion = input('Do you want to wait another 5 seconds \
                                                  for the chat acceptance? (N/y)')
                                if desicion == 'y':
                                    pass
                                elif desicion == 'N':
                                    print('Chat ended')
                                    break
                                else:
                                    print("You entered the wrong command! Try again after 5 seconds.")

                        while chat_started:
                            chat_message = input("Your message:")
                            if chat_message == '> exit':
                                print("Chat ended")
                                break
                            command_to_send = {'action': command,
                                               'status': "Chatting",
                                               'admin_id': admin_id,
                                               'message': chat_message}
                            login_response = client.send_dict_to_server(
                                data_dict=command_to_send)
                            login_response = login_response.decode('utf-8')
                            print(f"{admin_id}'s message: {login_response['message']}")

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
                        send_data = getpass.getpass("Enter new email:")

                        command_to_send = {'action': command,
                                           'email': send_data}
                        login_response = client.send_dict_to_server(
                            data_dict=command_to_send)
                        print(login_response.decode('utf-8'))

                    if command == "change_phoneNumber":
                        send_data = getpass.getpass("Enter new phone Number:")

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

                    if command == "add_screens" and local_client_settings.get_is_admin():
                        pass

        elif response == "Incorrect Password":
            print("You Enter wrong Password ")
        else:
            print("Print Signup first")

    finally:
        client.close_connection()


if __name__ == "__main__":
    main()
