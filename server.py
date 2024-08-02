import socket
import threading #sequence of instructions in a program that can be executed independently of the remaining process

# Function to handle communication with a connected client
def handle_client(client_socket, clients, usernames):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Broadcast the received message to all other clients
            broadcast(message, client_socket, clients, usernames)
        except:
            # Handle any exceptions and remove the client
            remove_client(client_socket, clients, usernames)
            break

# Function to broadcast messages to all clients except the sender
def broadcast(message, client_socket, clients, usernames):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Handle exceptions and remove the client if sending fails
                remove_client(client, clients, usernames)

# Function to remove a client from the list of connected clients
def remove_client(client_socket, clients, usernames):
    if client_socket in clients:
        index = clients.index(client_socket)
        username = usernames[index]
        clients.remove(client_socket)
        usernames.remove(username)
        # Notify all clients that the user has left the chat
        broadcast(f"{username} has left the chat.", client_socket, clients, usernames)

# Main function to set up the server and accept new client connections
def main():
    # Create a socket object for the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to an address and port
    server_socket.bind(('0.0.0.0', 5555))
    # Listen for incoming connections
    server_socket.listen(5)
    print("Server started on port 5555")

    clients = []
    usernames = []

    while True:
        # Accept a new client connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Request the username from the client
        client_socket.send("USERNAME".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8')
        clients.append(client_socket)
        usernames.append(username)

        print(f"{username} has joined the chat.")
        # Notify all clients that a new user has joined the chat
        broadcast(f"{username} has joined the chat.", client_socket, clients, usernames)
        
        # Send a welcome message to the new client
        welcome_message = f"Welcome to the chat, {username}!"
        client_socket.send(welcome_message.encode('utf-8'))

        # Start a new thread to handle communication with the connected client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, clients, usernames))
        client_handler.start()

if __name__ == "__main__":
    main()
