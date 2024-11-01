import socket

def request_file(host='127.0.0.1', port=12345, file_path=''):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the file request
    client_socket.send(file_path.encode())

    # Check if the file exists on the server
    response = client_socket.recv(1024).decode()
    if response == "FILE_FOUND":
        with open('received_' + file_path.split('/')[-1], 'wb') as f:
            # Receive the file in chunks
            while chunk := client_socket.recv(1024):
                f.write(chunk)
        print(f"File '{file_path}' received and saved as 'received_{file_path.split('/')[-1]}'.")
    else:
        print("ERROR: File not found on server")

    client_socket.close()

if __name__ == "__main__":
    # Replace 'example.txt' with the path to the file you want to request
    request_file(file_path='example.txt')