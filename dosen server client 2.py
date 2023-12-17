import socket
import threading

class BankServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def handle_client(self, client_socket):
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode()

            if not data:
                break  # Connection closed by client

            # Process the received data (implement your logic here)
            response = self.process_data(data)

            # Send a response back to the client
            client_socket.send(response.encode())

        # Close the client socket when the loop exits
        client_socket.close()

    def process_data(self, data):
        # Implement your server-side logic based on the received data
        # For simplicity, the server echoes the received data back to the client
        return f"Server received: {data}"

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            # Wait for a client to connect
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Handle the client in a separate thread
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = BankServer(host, port)
    server.start()
