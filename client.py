import socket


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_ip, server_port))

    def send_data(self, data):
        self.socket.sendall(data.encode())

    def receive_data(self):
        return self.socket.recv(1024).decode()

    def close(self):
        self.socket.close()


# Create a Client instance
# client = Client('localhost', 12345)
#
# # Send and receive data with the server
# client.send_data('Hello, server!')
# response = client.receive_data()
# print(f'Response from server: {response}')
#
# # Close the connection
# client.close()
