import socket
import json
import argparse
import getpass
from intractions import interation_commands
from settings import local_settings


class TCPClient:
    # Initialize connection
    def __init__(
            self,
            host=local_settings.Network['host'],
            port=local_settings.DATABASE['port']):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_dict_to_server(self, data_dict):
        json_string = json.dumps(data_dict)
        self.client_socket.sendall(json_string.encode('utf-8'))
        print(f"Sent dictionary to the server:\n{data_dict}")

        # Receive response from the server
        response = self.client_socket.recv(1024)
        print(f"Received response from the server: {response.decode('utf-8')}")
        return response

    def close_connection(self):
        self.client_socket.close()
        print("Connection closed.")


def show_services():
    for key, value in interation_commands.Interaction_Commands.items():
        print(key)


def main():
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
                'password': password}

        else:
            print("Invalid action.")
            return

        response = client.send_dict_to_server(data_dict=data_to_send)

        # Enter a loop to send commands after login
        if response == "Login successful!":
            while args.action == 'login':
                command = input(
                    "Enter a command or if you want to see all of our services enter -show services ")
                if command.lower() == 'logout':
                    break
                elif command == "-show services":
                    show_services()
                else:
                    data_to_send = {'command': command}
                    login_response = client.send_dict_to_server(
                        data_dict=data_to_send)
                    print(login_response)

        elif response == "Incorrect Password":
            print("You Enter wrong Password ")
        else:
            print("Print Signup first")

    finally:
        client.close_connection()


if __name__ == "__main__":
    main()
