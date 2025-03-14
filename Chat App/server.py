import socket
import threading

# Server setup
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Arbitrary port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            clients.remove(client)

def handle_client(client):
    """Handle messages from a single client."""
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                broadcast(message)
        except Exception as e:
            print(f"Error in handle_client: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    """Accept new client connections."""
    print("Server is listening...")
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}")
            broadcast(f"{nickname} joined the chat!".encode('utf-8'))
            client.send("Connected to the server!".encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error in receive: {e}")

if __name__ == "__main__":
    try:
        receive()
    except Exception as e:
        print(f"Error in starting server: {e}")
