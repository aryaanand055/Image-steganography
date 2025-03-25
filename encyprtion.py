from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

KEY_FILE = "aes_key.bin"

def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = os.urandom(32)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = get_key()

# Function to encrypt data
def encrypt_data_aes(data):
    data = data.encode()  # Convert the data to bytes
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the data to make it a multiple of 16 bytes
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to encrypted data

# Function to decrypt data
def decrypt_data_aes(encrypted_data):
    iv = encrypted_data[:16]  # Extract the IV from the encrypted data
    encrypted_content = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(encrypted_content) + decryptor.finalize()

    # Remove the padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_data


export = decrypt_data_aes, encrypt_data_aes
