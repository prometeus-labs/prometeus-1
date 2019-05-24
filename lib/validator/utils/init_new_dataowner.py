import json, ast
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cryptography
from cryptography.fernet import Fernet


def encrypt1(data):
    ret = {}
    key = RSA.generate(1024)
    
    publick_key = key.publickey().exportKey('PEM')
    private_key = key.exportKey('PEM')

    key = RSA.importKey(publick_key)
    key1 = RSA.importKey(private_key)
    
    print(key)
    print(key1)

    encryptor = PKCS1_OAEP.new(key)

    ret = {
        'encripted': encryptor.encrypt(json.dumps(data).encode()),
        'public_key': publick_key,
        'private_key': private_key
    }

    return ret


def decrypt1(encrypted, private_key):
    key = RSA.importKey(private_key)
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
    return decrypted

def encrypt2(data):
    key = Fernet.generate_key()
    data = json.dumps(data).encode()

    encrypted = Fernet(key).encrypt(data)   

    ret = {
        'encrypted': encrypted,
        'private_key': key
    }

    return ret

def decrypt2(data, private_key):
    f = Fernet(private_key)
    decrypted = f.decrypt(data)
    return decrypted

