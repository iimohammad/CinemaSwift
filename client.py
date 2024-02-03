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
    def __init__(self, host='127.0.0.1', port=8080) :
        self.client = TCPClient(host, port)
        self.username = None
        self.is_logged_in = False
    
    def signup(self,username):
        
        if not self.is_logged_in:
            data_to_send = {'action': 'signup', 'username': username}
            self.client.connect()
            response = self.client.send_dict_to_server(data_dict=data_to_send)
            if response.get('status') == 'success':
                print(f"User '{username}' successfully signed up.")
            else:
                print(f"Error: {response.get('error_message')}")
        else:
            print("Error: You are already logged in. Logout first.")

    def login(self,username,password):

        if not self.is_logged_in:
            data_to_send = {'action': 'login', 'username': username, 'password': password}
            self.client.connect()
            self.client.send_dict_to_server(data_to_send)
            response = json.loads(self.client.client_socket.recv(1024).decode('utf-8'))
            self.client.close_connection()

            if response.get('status') == 'success':
                self.is_logged_in = True
                self.username = username
                print(f"Logged in as {username}")
            else:
                print("Login failed. Check your username and password.")
        else:
            print("Error: You are already logged in. Logout first.")

    def is_login(self) :
       
        return self.is_logged_in
    
    def is_manager(self):

        if self.is_logged_in:
            data_to_send = {'action': 'is_manager', 'username': self.username}
            self.client.connect()
            self.client.send_dict_to_server(data_to_send)
            response = json.loads(self.client.client_socket.recv(1024).decode('utf-8'))
            self.client.close_connection()
            return response.get('is_manager', False)
        else:
            print("Error: You are not logged in.")
            return False
        
    def help(self):

        print("Available commands:")
        print("  signup <username>")
        print("  login <username> <password>")
        print("  is_login")
        print("  is_manager")
        print("  help")



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
