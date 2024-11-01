import socket
import os

def start_server(host='0.0.0.0', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Receive the file request
        file_path = client_socket.recv(1024).decode()
        print(f"Client requested file: {file_path}")

        # Check if the file exists
        if os.path.isfile(file_path):
            client_socket.send(b"FILE_FOUND")
            with open(file_path, 'rb') as f:
                # Send the file in chunks
                while chunk := f.read(1024):
                    client_socket.send(chunk)
            print(f"File '{file_path}' sent to client.")
        else:
            client_socket.send(b"ERROR: File not found")

        client_socket.close()

if __name__ == "__main__":
    start_server()