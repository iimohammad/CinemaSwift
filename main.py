import argparse
import threading
import socket
import json
from users_module.users import Users
from db import models
from intractions import clear_screen
from intractions import interation_commands
from settings import local_settings
from db import initialize_all_module
from intractions import server_commands


def configDB():
    initialize_all_module.run()


class UserDatabase:
    users = {}

    @classmethod
    def check_credentials(cls, username, password):
        return cls.users.get(username) == password


class ClientThread(threading.Thread):
    def __init__(self, client_socket, server):
        super(ClientThread, self).__init__()
        self.client_socket = client_socket
        self.server = server

    def run(self):

        data = self.client_socket.recv(1024).decode('utf-8')
        try:
            self.server.parse_data(data, self.client_socket)
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
        finally:
            self.client_socket.close()


class TCPServer:
    def __init__(
            self,
            host=local_settings.Network['host'],
            port=local_settings.Network['port']):
        self.host = host
        self.port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.logged_in_users = {}
        self.lock = threading.Lock()

    def run_server(self):
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_thread = ClientThread(client_socket, self)
                client_thread.start()
        except KeyboardInterrupt:
            print("Server interrupted. Closing...")
        finally:
            self.server_socket.close()

    def parse_data(self, received_data, client_socket):

        global response
        data_dict = json.loads(received_data)

        action = data_dict.get('action')
        username = data_dict.get('username')
        response = "Invalid action!"
        if action == 'signup':
            # usernamea = data_dict['username']
            password = data_dict['password']
            email = data_dict['email']
            phone = data_dict['phone']
            birthday = data_dict['birthday']

            user = models.user_model(
                -1,
                username=username,
                email=email,
                birthday=birthday,
                phone=phone,
                subscription_type_id=1,
                password=password,
                is_admin=0)

            try:
                Users.AddUser(user=user)
                response = "Signup successful!"
            except Exception as e:
                print(response)
                # response=response.encode('utf-8')

        elif action == 'login':
            username = data_dict['username']
            password = data_dict['password']
            user_id = Users.log_in(username, password)
            if user_id:
                print(f"User '{username}'Login successful!")
                with self.lock:
                    self.logged_in_users[client_socket] = username

                if Users.is_admin(user_id):
                    response = "Admin Login successful"
                response = "Login successful!"

                while True:
                    client_socket.sendall(response.encode('utf-8'))
                    # Continuously receive and process data from the client
                    received_data = client_socket.recv(1024).decode('utf-8')
                    data_dict_command = json.loads(received_data)
                    final_command = data_dict_command['action']

                    if Users.is_admin(user_id):
                        try:
                            # This part use for admin users
                            if final_command in interation_commands.interactions_commands:
                                print("find")
                                response = interation_commands.interactions_commands[final_command](
                                    user_id, data_dict_command)
                                # client_socket.sendall(response.encode('utf-8'))
                        except:
                            response = "Not find this Command"
                    else:
                        # This part is use for normal users
                        try:
                            if final_command in interation_commands.interactions_commands:
                                print("find")
                                response = interation_commands.interactions_commands[final_command](
                                    username, data_dict_command)

                        except:
                            response = "Not find this Command"

            else:
                print(f"Login failed for user '{username}'")
                response = "Login failed. Check your credentials."
            print(self.logged_in_users)

        else:
            response = "Please log in first!"

        client_socket.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TCP Server")
    parser.add_argument(
        '--runserver',
        action='store_true',
        help='Run the TCP server')

    parser.add_argument(
        '--addAdmin',
        action='store_true',
        help='Add an admin'
    )
    parser.add_argument(
        '--configDB',
        action='store_true',
        help='Add an admin'
    )

    parser.add_argument(
        '--show-user-manual',
        action='store_true',
        help='Add an admin'
    )

    parser.add_argument(
        '--change-to-admin',
        action='store_true',
        help='Add an admin'
    )
    args = parser.parse_args()

    clear_screen.clear_screen_func()

    if args.runserver:
        clear_screen.clear_screen_func()
        server = TCPServer()
        server.run_server()

    if args.addAdmin:
        clear_screen.clear_screen_func()
        server_commands.signup_admin()

    if args.configDB:
        clear_screen.clear_screen_func()
        configDB()

    if args.show_user_manual:
        clear_screen.clear_screen_func()
        server_commands.help_print()

    if args.change_to_admin:
        clear_screen.clear_screen_func()
        username = input("Enter the username you want to change to admin:")
        server_commands.change_user_to_admin(username)
