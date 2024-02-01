import socket
import threading

def handle_client(client_socket):
    
    data = client_socket.recv(1024)
    response = b"Hello from the server!\n"
    client_socket.send(response)
    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))
server.listen(5)

print("[*] Listening on 0.0.0.0:12345")

while True:
    client, addr = server.accept()
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

    
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

