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

        if data_dict['action'] == 'signup':
            username = data_dict['username']
            password = data_dict['password']
            email = data_dict['email']
            phone = data_dict['phone']
            birthday = data_dict['birthday']

            # Perform signup logic
            user = models.user_model(
                1,
                username=username,
                email=email,
                birthday=birthday,
                phone=phone,
                password=password)
            print(user.username)
            birthday = datetime(year=1990, month=1, day=1)

            print("--------------------")
            # Users.AddUser(
            #     models.user_model(
            #         id=1,
            #         username="Masih11",
            #         email="john@example.com",
            #         birthday=birthday,
            #         phone="09125397806",
            #         password="Mail1375#@#"))

            Users.AddUser(user=user)
            UserDatabase.users[username] = password

            print(f"User '{username}' signed up successfully with email {
                  email}, phone {phone}, and birthday {birthday}!")
            response = "Signup successful!"

        elif data_dict['action'] == 'login':
            username = data_dict['username']
            password = data_dict['password']

            # Perform login logic
            if UserDatabase.check_credentials(username, password):
                print(f"User '{username}' logged in successfully!")
                response = "Login successful!"
            else:
                print(f"Login failed for user '{username}'")
                response = "Login failed. Check your credentials."

        else:
            response = "Invalid action!"

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
