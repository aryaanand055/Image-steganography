import base64
from PIL import Image
from encyprtion import encrypt_data_aes, decrypt_data_aes

# Convert encoding data into 8-bit binary
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Get a new filename for the encoded image
def getNewFileName(filename):
    return filename.split(".")[0] + "_encoded.png"

# Convert the image pixels to binary and modify the least significant bit
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                         imdata.__next__()[:3] +
                         imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                pix[j] += -1 if pix[j] != 0 else 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] += -1 if pix[-1] != 0 else 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# Encode the data into the image
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode_data():
    img = input("🖼️\t Enter image name (with extension): ")
    image = Image.open(img, 'r')

    max_bytes = image.size[0] * image.size[1] // 3
    print(f"ℹ️ The maximum characters that can be encoded are: {max_bytes}")
    
    input_data = input("🔤 \tEnter data to be encoded: ")
    encrypted_data = encrypt_data_aes(input_data)
    
    # Convert encrypted data to Base64 for safe storage in image
    encoded_string = base64.b64encode(encrypted_data).decode()
    
    if len(encoded_string) == 0:
        raise ValueError('❌ Data is empty')

    newimg = image.copy()
    encode_enc(newimg, encoded_string)

    new_img_name = getNewFileName(img)
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    print(f"✅ The image is encoded successfully and stored as {new_img_name}")

# Decode the data in the image
def decode_data():
    img = input("Enter image name(with extension): ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                               imgdata.__next__()[:3] +
                               imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))

        if pixels[-1] % 2 != 0:
            break

    # Convert Base64 back to encrypted bytes and decrypt
    decrypted_data = decrypt_data_aes(base64.b64decode(data))
    return decrypted_data.decode()

def main():
    a = int(input(":: Welcome to Steganography ::\n"
                  "1️⃣\t Encode\n2️⃣\t Decode\nMake sure to use only PNG images.\n:"))
    if a == 1:
        encode_data()
    elif a == 2:
        print("🔍 \tDecoded Message: " + decode_data())
    else:
        raise Exception("❌ Enter correct input")

if __name__ == '__main__':
    main()
