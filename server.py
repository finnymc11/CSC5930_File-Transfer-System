import socket
import threading
import os

HEADER = 64
PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) 
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()


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
