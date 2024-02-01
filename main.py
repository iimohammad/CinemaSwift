import argparse
import socket
import threading

def create_admin():
    print("Creating admin...")

def argsinput():
    parser = argparse.ArgumentParser(description='Script for various operations')
    parser.add_argument('command', help='Specify the command to execute')

    args = parser.parse_args()

    if args.command == 'create_admin':
        create_admin()
    else:
        print(f"Unknown command: {args.command}")




def handle_client(client_socket, user_data):
    while True:
        request = client_socket.recv(1024).decode()

        if request.lower() == 'logout':
            break

        response = f"Server received: {request}"
        client_socket.send(response.encode())

    print(f"User {user_data['username']} logged out.")
    user_data['logged_in'] = False
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)

    print("Server listening on 0.0.0.0:12345")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        user_data = {'username': 'sample_user', 'logged_in': True}

        client_handler = threading.Thread(target=handle_client, args=(client, user_data))
        client_handler.start()

if __name__ == "__main__":
    argsinput()
    main()


