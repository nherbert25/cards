import socket
import threading

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Get IP Address from current machine
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

# Define the server port
PORT = 5001

# Bind the socket to the IP and port
server_socket.bind((IP, PORT))

# Listen for incoming connections
server_socket.listen()
print('Server started. Waiting for incoming connections...')

# List of connected clients
clients = []


# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    # Add the client to the list of connected clients
    clients.append(client_socket)

    # Send a welcome message to the client
    client_socket.send("Welcome to the server!\n".encode())

    while True:
        # Receive messages from the client
        message = client_socket.recv(1024)

        # Broadcast the message to all connected clients
        for client in clients:
            if client != client_socket:
                client.send(f"{client_address}: {message.decode()}".encode())

        # If the client disconnected, remove it from the list of connected clients
        if not message:
            clients.remove(client_socket)
            client_socket.close()
            break


# Main loop to handle incoming client connections
while True:
    # Wait for incoming client connectionsnetwo
    client_socket, client_address = server_socket.accept()
    print(f'New client connected: {client_address}')


    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
    # clients.append(client_address)
##