import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
host = socket.gethostbyname(socket.gethostname())
port = 5001

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to server {host}:{port}")

# Send a message to the server
message = "Hello, Server!"
client_socket.send(message.encode('utf-8'))

# Receive the server's response
response = client_socket.recv(1024).decode('utf-8')
print(f"Response from server: {response}")

# Close the connection
client_socket.close()
