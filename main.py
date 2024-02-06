import argparse
import threading
import socket
import json
from users_module.users import Users
from db import models
from intractions import clear_screen
from intractions import interation_commands
from datetime import datetime
from settings import local_settings


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
        # print(received_data)
        data_dict = json.loads(received_data)

        action = data_dict.get('action')
        username = data_dict.get('username')

        if action == 'signup':
            print("------------------")
            username = data_dict['username']
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
                password=password)

            # print(user)
            Users.AddUser(user=user)

            response = "Signup successful!"

        elif action == 'login':
            username = data_dict['username']
            password = data_dict['password']
            # print(username,password)
            # print( Users.log_in(username, password))

            if Users.log_in(username, password):
                print(f"User '{username}'Login successful!")
                with self.lock:
                    self.logged_in_users[client_socket] = username

                response = "Login successful!"
                while True:
                    client_socket.sendall(response.encode('utf-8'))
                    # Continuously receive and process data from the client
                    received_data = client_socket.recv(1024).decode('utf-8')
                    data_dict_command = json.loads(received_data)
                    finalCommand = data_dict_command['action']
                    if finalCommand in interation_commands.Interaction_Commands:
                        response = interation_commands.Interaction_Commands[finalCommand](
                        )
            else:
                print(f"Login failed for user '{username}'")
                response = "Login failed. Check your credentials."
            print(self.logged_in_users)

        elif client_socket in self.logged_in_users:
            # elif  action == 'change_username':
            print("hi")
            # print("hi")
            # print (action)
            # if action in interation_commands.Interaction_Commands:
            #     response = interation_commands.Interaction_Commands[action]()
            # else:
            #     response = "Invalid action!"

        else:
            response = "Please log in first!"

        print(response)
        client_socket.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TCP Server")
    parser.add_argument(
        '--runserver',
        action='store_true',
        help='Run the TCP server')

    args = parser.parse_args()

    clear_screen.clear_screen_func()

    if args.runserver:
        server = TCPServer()
        server.run_server()
