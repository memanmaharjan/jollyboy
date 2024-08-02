import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            # Receive message from the server
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Print the received message
            print(message)
        except:
            # Handle any exceptions and close the client socket
            print("An error occurred.")
            client_socket.close()
            break

def main():
    # Create a socket object for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect(('127.0.0.1', 5555))

    # Prompt the user to enter their username
    username = input("Enter your username: ")
    # Send the username to the server
    client_socket.send(username.encode('utf-8'))

    # Start a new thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Read a message from the user
        message = input()
        # Check if the user wants to exit
        if message.lower() == 'exit':
            # Send a message to the server indicating that the user has left the chat
            client_socket.send(f"{username} has left the chat.".encode('utf-8'))
            # Close the client socket
            client_socket.close()
            break
        else:
            # Send the user's message to the server
            client_socket.send(f"{username}: {message}".encode('utf-8'))

if __name__ == "__main__":
    main()
