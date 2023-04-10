import socket

# Define the server's IP address and port
SERVER_IP = '192.168.68.115'
SERVER_PORT = 5001

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

while True:
    # Send a message to the server
    message = input("Enter message to send to server: ")
    client_socket.sendall(message.encode())

    # Receive a response from the server
    data = client_socket.recv(1024)
    print(f"Received from server: {data.decode()}")

# Close the socket
client_socket.close()
