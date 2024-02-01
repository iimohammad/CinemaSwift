import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))

    while True:
        request = input("Enter your request (or 'logout' to exit): ")
        client.send(request.encode())

        if request.lower() == 'logout':
            break

        response = client.recv(1024).decode()
        print(f"Server response: {response}")

    client.close()

if __name__ == "__main__":
    main()
