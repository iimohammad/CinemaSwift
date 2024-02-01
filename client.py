import socket
import json
import argparse
class TCPClient:
    def __init__(self, host='127.0.0.1', port=8080):
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

    def close_connection(self):
        self.client_socket.close()
        print("Connection closed.")



class handle_users:
    def __init__(self) -> None:
        pass
    
    def signup(self,username):
        pass
    def login(self,username,password):
        pass

    def is_login(self) -> bool:
        pass

    def is_manager(self) -> bool:
        pass
    def help(self):
        pass

class manager_services:
    def __init__(self,username) -> None:
        self.username = username

    def add_showtimes(self):
        pass


class users_services:
    def __init__(self,username) -> None:
        self.username = username

    def reserve_showtime(self):
        pass



def main():
    parser = argparse.ArgumentParser(description="Client for Movie Reservation System")
    parser.add_argument('action', choices=['signup', 'login'], help='Specify the action to perform (signup or login)')
    parser.add_argument('--username', help='Specify the username for signup or login')

    args = parser.parse_args()

    if args.action == 'signup':
        if not args.username:
            print("Error: Username is required for signup.")
            return
        client = TCPClient()
        try:
            client.connect()
            data_to_send = {'action': 'signup', 'username': args.username}
            client.send_dict_to_server(data_dict=data_to_send)
        finally:
            client.close_connection()

    elif args.action == 'login':
        if not args.username:
            print("Error: Username is required for login.")
            return
        # Perform login
        client = TCPClient()
        try:
            client.connect()
            data_to_send = {'action': 'login', 'username': args.username}
            client.send_dict_to_server(data_dict=data_to_send)
        finally:
            client.close_connection()


if __name__ == "__main__":
    main()
