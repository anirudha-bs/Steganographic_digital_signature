import cv2
import numpy as np
import re
import digital_sign


def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode():
    path = input("Enter the image path (Only png supported) - ")
    image = cv2.imread(path)
    data = input("Enter the message to digitally sign it - ")
    signature, public_key = digital_sign.sign(data)
    pub_key = public_key.exportKey()
    secret_data = str(signature) + ">>>>>" + str(pub_key) + "*****"
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    data_index = 0
    binary_secret_data = to_bin(secret_data)
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image


def decode():
    path = input("Enter the path of the image to verify - ")
    data = input("Enter the the data to be verified - ")
    image = cv2.imread(path)
    print("[+] Decoding...")
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*****":
            break

    sign = decoded_data[:-5]
    sign = re.split('>>>>>', sign)
    signature = sign[0][2:-1]
    pub_key = sign[1][2:-1]
    public_key = pub_key.replace('\\n', '\n')
    result = digital_sign.verify(signature=signature, public_key=public_key, data=data)
    return result
