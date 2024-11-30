import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# AES key for encryption (must be 16, 24, or 32 bytes)
key = b'This is a key123'  # Ensure the key length is correct

def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(data.encode(), AES.block_size)
    cipher_text = cipher.encrypt(padded_text)
    return iv + cipher_text

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(1)
    print("Server listening on port 9999")

    while True:
        print("Waiting for a connection...")
        client_socket, addr = server_socket.accept()
        print(f"Connected by {addr}")

        try:
            # Receive the filename from the client
            filename = client_socket.recv(1024).decode()
            print(f"Client requested file: {filename}")

            if os.path.isfile(filename):
                with open(filename, "rb") as file:
                    data = file.read()
                    # TODO: Encrypt the file data before sending
                    cipher_text = encrypt_data(data, key)
                    print(f"Encrypted text (in bytes): {cipher_text}")
                    # TODO: Send encrypted data to the client
                    client_socket.send(cipher_text)
                print(f"File '{filename}' sent to the client.")
            else:
                client_socket.send("File not found.".encode())
                print("File not found.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print("Connection closed.")

start_server()