from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from base64 import b64decode
from base64 import b64encode


def sign(data):
    try:
        f = open('mykey.pem', 'rb')
    except IOError:
        private_key = RSA.generate(2048)
        f = open('mykey.pem', 'wb')
        f.write(private_key.exportKey('PEM'))
    finally:
        f.close()

    f = open('mykey.pem', 'rb')
    private_key = RSA.importKey(f.read())
    public_key = private_key.publickey()

    h = SHA256.new(data.encode('utf-8'))
    signer = PKCS1_v1_5.new(private_key)
    signature = b64encode(signer.sign(h))
    print("----- Your digital signature -----")
    print(signature)
    print("----- Your digital signature -----")
    print("----- Your public key -----")
    print(public_key)
    print("----- Your public key -----")
    return signature, public_key


def verify(signature,public_key, data):
    print("----- Digital signature -----")
    print(signature)
    print("----- Digital signature -----")
    print("----- Signer's public key -----")
    print(public_key)
    print("----- Signer's public key -----")
    rsakey = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data.encode('utf-8'))
    if signer.verify(digest, b64decode(signature)):
        return True
    else:
        return False
