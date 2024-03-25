import socket
import time
import random


class ClientAI:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port

    def send_data(self):
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        try:
            for _ in range(6):  # Send data every 10 seconds for 1 minute
                number = random.uniform(-10, 10)  # Send a random number between -10 and 10
                print(f"Sent data: {number}")
                client_socket.sendall(str(number).encode())
                time.sleep(10)
        finally:
            client_socket.close()

        print("Data transfer completed.")


# Create an instance of ClientAI and send data to the server
client = ClientAI()
client.send_data()
