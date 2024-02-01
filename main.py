import argparse
import threading
import os
import selectors
import socket
from settings import local_settings
from intractions import clear_screen

class TCPServer:
    def __init__(self, host=local_settings.Network['host'], port=local_settings.Network['port']):
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
            else:
                print(f"Closing connection to {client_socket.getpeername()}")
                self.sel.unregister(client_socket)
                client_socket.close()

        if mask & selectors.EVENT_WRITE:
            if data:
                sent = client_socket.send(data)
                data = data[sent:]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run TCP Server")
    parser.add_argument('--runserver', action='store_true', help='Run the TCP server')

    args = parser.parse_args()
    
    # Use the imported clear_screen function
    clear_screen.clear_screen_func()

    if args.runserver:
        server = TCPServer()
        server.run_server()
