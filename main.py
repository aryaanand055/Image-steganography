from PIL import Image
from files import create_file, get_text_file
from encryption import encrypt_data_aes, decrypt_data_aes
from colorama import Fore, Style, init

init(autoreset=True)

def genData(data):
    return [format(ord(i), '08b') for i in data]

def getNewFileName(filename):
    return filename.rsplit(".", 1)[0] + "_e.png"

def modPix(pix, data):
    datalist = genData(data)
    imdata = iter(pix)
    for i, binary_char in enumerate(datalist):
        try:
            pixel_values = sum([list(next(imdata)[:3]) for _ in range(3)], [])
        except StopIteration:
            raise ValueError(Fore.RED + "Error: Image too small to hold all data.")

        for j in range(8):
            if (binary_char[j] == '0' and pixel_values[j] % 2):
                pixel_values[j] -= 1
            elif (binary_char[j] == '1' and pixel_values[j] % 2 == 0):
                pixel_values[j] += 1 if pixel_values[j] < 255 else -1

        pixel_values[-1] = pixel_values[-1] | 1 if i == len(datalist) - 1 else pixel_values[-1] & ~1
        yield tuple(pixel_values[:3])
        yield tuple(pixel_values[3:6])
        yield tuple(pixel_values[6:9])

def encode_enc(newimg, data):
    w = newimg.size[0]
    x = y = 0
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        x = 0 if x == w - 1 else x + 1
        y += 1 if x == 0 else 0

def encode_data():
    print(f"\n{Fore.CYAN}--- Encoding Mode ---{Style.RESET_ALL}")
    img = input("Enter image name (with extension): ")
    image = Image.open(img)
    max_bytes = image.size[0] * image.size[1] // 3
    print(f"{Fore.YELLOW}Maximum characters that can be encoded: {max_bytes}{Style.RESET_ALL}")

    input_mode = input("Choose input mode - File (F) or Manual (M): ").lower()
    if input_mode == 'f':
        file_path = input("Enter the file path: ")
        input_data = get_text_file(file_path)
    else:
        input_data = input("Enter data to encode: ")

    encoded_string = encrypt_data_aes(input_data)

    if len(encoded_string) == 0:
        raise ValueError(Fore.RED + "Error: Cannot encode empty data.")
    if len(encoded_string) > max_bytes:
        raise ValueError(Fore.RED + f"Error: Data exceeds image capacity ({max_bytes} characters max).")

    newimg = image.copy()
    encode_enc(newimg, encoded_string)

    new_img_name = getNewFileName(img)
    newimg.save(new_img_name, "PNG")
    print(f"{Fore.GREEN}Success: Image encoded and saved as '{new_img_name}'{Style.RESET_ALL}")

def decode_data():
    print(f"\n{Fore.CYAN}--- Decoding Mode ---{Style.RESET_ALL}")
    img = input("Enter image name (with extension): ")
    image = Image.open(img)
    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = sum([list(next(imgdata)[:3]) for _ in range(3)], [])
        binstr = ''.join(['1' if i % 2 else '0' for i in pixels[:8]])
        data += chr(int(binstr, 2))
        if pixels[-1] % 2:
            break

    print(f"\n{Fore.MAGENTA}[Debug] Extracted encrypted data (first 100 chars): {data[:100]}{Style.RESET_ALL}")

    decrypted_data = decrypt_data_aes(data)
    action = input("\nSave to file (S) or Print (P): ").lower()
    if action == 's':
        filename = input("Enter filename to save output: ")
        create_file(decrypted_data.decode(), filename)
        print(f"{Fore.GREEN}Success: Data saved to '{filename}'{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}Decoded Data:\n{Style.RESET_ALL}{decrypted_data.decode()}")

def main():
    print(f"{Fore.BLUE}Secure Image Steganography\n{Style.RESET_ALL}Supported formats: {Fore.YELLOW}Image - PNG, Data - TXT\n{Style.RESET_ALL}")
    option = input("1. Encode\n2. Decode\n\nEnter Option (1 or 2): ")
    if option == '1':
        encode_data()
    elif option == '2':
        decode_data()
    else:
        print(Fore.RED + "Invalid option selected.")

if __name__ == '__main__':
    main()
