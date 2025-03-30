
# Image Steganography with AES Encryption

This project implements a secure image steganography system that allows users to encode and decode secret messages into PNG images. The messages are encrypted using AES encryption for added security.

## Features

1. **Image Steganography**S:
   - Encode secret messages into PNG images by modifying the least significant bits of pixel values.
   - Decode messages from encoded images.

2. **AES Encryption**:
   - Encrypt messages using AES encryption in CBC mode before encoding them into images.
   - Decrypt messages after decoding them from images.

3. **Neural Network (Experimental)**:
   - A simple deep neural network implementation (`neuralNetwork.py`) for potential use in advanced steganography or other tasks.

## File Descriptions

### `main.py`
- The main entry point of the application.
- Provides a menu-driven interface for encoding and decoding messages.
- Functions:
  - `encode_data()`: Encodes a user-provided message into a PNG image.
  - `decode_data()`: Decodes and decrypts a message from an encoded PNG image.

### `encryption.py`
- Handles AES encryption and decryption of messages.
- Functions:
  - `encrypt_data_aes(data)`: Encrypts a message using AES encryption.
  - `decrypt_data_aes(encrypted_data_base64)`: Decrypts an AES-encrypted message.
- Automatically generates and stores a 256-bit AES key in `aes_key.bin`.

### `neuralNetwork.py`
- Implements a simple deep neural network for experimental purposes.
- Functions:
  - `train(training_inputs, training_outputs, num_iterations, learning_rate)`: Trains the neural network.
  - `think(inputs)`: Makes predictions using the trained network.
- Example usage: Approximates the function `x^2` for normalized inputs.

### `aes_key.bin`
- A binary file that stores the AES encryption key. Automatically generated if not present.

### `readme.md`
- This documentation file.

## How to Use

1. **Setup**:
   - Ensure you have Python installed.
   - Install required dependencies:
     ```bash
     pip install pillow cryptography numpy
     ```

2. **Run the Application**:
   - Execute `main.py`:
     ```bash
     python main.py
     ```

3. **Encode a Message**:
   - Select the "Encode" option.
   - Provide the path to a PNG image and the message to encode.
   - The encoded image will be saved with `_encoded` appended to its name.

4. **Decode a Message**:
   - Select the "Decode" option.
   - Provide the path to an encoded PNG image.
   - The decoded and decrypted message will be displayed.

## Notes

- Only PNG images are supported for encoding and decoding.
- The maximum message size depends on the image dimensions (1 character per 3 pixels).
- The neural network implementation is independent of the steganography functionality and is included for experimental purposes.

## Example

### Encoding
```plaintext
:: Welcome to Secure image Steganography ::
1. Encode
2️. Decode
Make sure to use only PNG images.
: 1
🖼️ Enter image name (with extension): example.png
ℹ️ The maximum characters that can be encoded are: 10000
🔤 Enter data to be encoded: Hello, World!
✅ The image is encoded successfully and stored as example_encoded.png
```

### Decoding
```plaintext
:: Welcome to Secure image Steganography ::
1. Encode
2️. Decode
Make sure to use only PNG images.
: 2
Enter image name(with extension): example_encoded.png
🔍 Decoded Message: Hello, World!
```

## License

This project is open-source and available for educational purposes. Use it responsibly.

