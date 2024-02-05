import argparse
import threading
import os
import selectors
import socket
from settings import local_settings
from intractions import clear_screen
from intractions import interation_commands
import json
from users_module.users import Users
from db import models
from datetime import datetime


class UserDatabase:
    users = {}

    @classmethod
    def check_credentials(cls, username, password):
        return cls.users.get(username) == password


class TCPServer:
    def __init__(
            self,
            host=local_settings.Network['host'],
            port=local_settings.Network['port']):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.login_clients = {}

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        server_socket.setblocking(False)
        self.sel.register(server_socket, selectors.EVENT_READ, data=None)

        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_connection(key.fileobj)
                    else:
                        self.handle_data(key, mask)
        finally:
            self.sel.close()

    def accept_connection(self, server_socket):
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = {'socket': client_socket, 'data': b''}
        self.sel.register(client_socket, events, data=data)

    def handle_data(self, key, mask):
        client_socket = key.fileobj
        data = key.data['data']

        if mask & selectors.EVENT_READ:
            recv_data = client_socket.recv(1024)
            if recv_data:
                data += recv_data
                try:
                    self.parse_data(data.decode('utf-8'), client_socket)
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON data: {e}")

            else:
                print(f"Closing connection to {client_socket.getpeername()}")
                self.sel.unregister(client_socket)
                client_socket.close()
                return  # Exit early if no data received

        if mask & selectors.EVENT_WRITE:
            if data:
                sent = client_socket.send(data)
                data = data[sent:]

    def parse_data(self, received_data, client_socket):
        data_dict = json.loads(received_data)

        action = data_dict.get('action')
        username = data_dict.get('username')  

        if action == 'signup':
            username = data_dict['username']
            password = data_dict['password']
            email = data_dict['email']
            phone = data_dict['phone']
            birthday = data_dict['birthday']

            # Perform signup logic
            user = models.user_model(
                -1,
                username=username,
                email=email,
                birthday=birthday,
                phone=phone,
                password=password)

            Users.AddUser(user=user)

            response = "Signup successful!"

        elif action == 'login':
            username = data_dict['username']
            password = data_dict['password']

            if Users.log_in(username, password):
                print(f"User '{username}' logged in successfully!")
                self.logged_in_users[client_socket] = username
                response = "Login successful!"
            else:
                print(f"Login failed for user '{username}'")
                response = "Login failed. Check your credentials."

        elif client_socket in self.logged_in_users:
            if action in interation_commands.Interaction_Commands:
                function_name = interation_commands.Interaction_Commands[action]
                # response = getattr(interation_commands, function_name)(username)
                response = function_name(username,*argparse)
            else:
                response = "Invalid action!"

        else:
            # User is not logged in, deny certain actions
            response = "Please log in first!"

        # Print the response
        print(response)

        # Send response to the client
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
