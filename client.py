import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# AES key for decryption (must match the server's key)
key = b'This is a key123'  # Ensure the key length is correct

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_text = cipher.decrypt(encrypted_data[AES.block_size:])
    decrypted_text = unpad(decrypted_padded_text, AES.block_size)
    return decrypted_text.decode()

def request_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(ADDR)
        
    try:
        # Send the filename to the server
        client_socket.send(filename.encode())
        print(f"Requested file: {filename}")

        # Receive the encrypted data from the server
        encrypted_data = b''
        while True:
            part = client_socket.recv(1024)
            if not part:
                break
            encrypted_data += part
        
        # TODO: Decrypt the received data
        decrypted_text = decrypt_data(encrypted_data, key)
        print(f"Decrypted text: {decrypted_text}")
        # TODO: Save the decrypted data to a file
        output_filename = f"decrypted_{filename}"  # Save as a new file
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(decrypted_text)
        print(f"File '{output_filename}' received and saved.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

filename = input("Enter the filename to request: ")
request_file(filename)
