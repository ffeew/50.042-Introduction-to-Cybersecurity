from Crypto.PublicKey import RSA
import math
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS

def generate_RSA(bits=1024):
    private_key = RSA.generate(bits)
    public_key = private_key.publickey()
    return private_key.exportKey(), public_key.exportKey()


keys = generate_RSA()
# store the public keys into a file
with open("public_key_file", "wb") as fout:
    fout.write(keys[1])
# store the private keys into a file
with open("private_key_file", "wb") as fout:
    fout.write(keys[0])

def encrypt_RSA(public_key_file,message):
    with open(public_key_file, "rb") as fin:
        key = fin.read()
        RSAkeys = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(RSAkeys)
        ciphertext = cipher.encrypt(message)
        return ciphertext

def decrypt_RSA(private_key_file,ciphertext):
    with open(private_key_file, "rb") as fin:
        key = fin.read()
        RSAkeys = RSA.importKey(key)
        cipher = PKCS1_OAEP.new(RSAkeys)
        message = cipher.decrypt(ciphertext)
        return message

def sign_data(private_key_file,data):
    with open(private_key_file, "rb") as fin:
        key = fin.read()
        RSAkeys = RSA.importKey(key)
        signer = PKCS1_PSS.new(RSAkeys)
        data_hash = SHA256.new(data)
        signature = signer.sign(data_hash)
        return signature

def verify_sign(public_key_file,sign,data):
    with open(public_key_file, "rb") as fin:
        key = fin.read()
        RSAkeys = RSA.importKey(key)
        signer = PKCS1_PSS.new(RSAkeys)
        data_hash = SHA256.new(data)
        verification = signer.verify(data_hash, signature = sign)
        return verification

def int_to_bytes(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little')

with open("mydata.txt", "rb") as fin:
    message = fin.read()
    print("message: ", message, "\n")
    ciphertext = encrypt_RSA("public_key_file", message)
    print("ciphertext: ", ciphertext, "\n")
    decrypted_ciphertext = decrypt_RSA("private_key_file", ciphertext)
    print("decrypted ciphertext: ", decrypted_ciphertext, "\n")
    signed_data = sign_data("private_key_file", message)
    print("Signature: ", signed_data, "\n")
    verification = verify_sign("public_key_file", signed_data, decrypted_ciphertext)
    print("Message verification: ", verification, "\n")

print("================= Commencing protocol attack on RSA with Padding =================")

data = int_to_bytes(100)

print("Data: ", data, "\n")
y1 = encrypt_RSA("public_key_file", data)
print("Original message: ", data, "\n")
print("encrypted original data", y1, "\n")

multiplier = int_to_bytes(2)
print("Multiplier: ", multiplier, "\n")
y2 = encrypt_RSA("public_key_file", multiplier)

y3 = int_to_bytes(int.from_bytes(y1, byteorder="little")*int.from_bytes(y2, byteorder="little"))

print("Ciphertext after multiplying with multiplier: ", y3, "\n")

try:
    decrypted_data = decrypt_RSA("private_key_file", y3)

except:
    print("Decryption Failed")


print("================= Commencing digital signature protocol attack on RSA with Padding =================")

# message would be encrypted in real life, but since the signature verification does not 
# need decryption of the message, message is left as plaintext for simplification.
message = b"This is from 'fake' Alice"
print("Message from Eve: ", message, "\n")
try:
    # sign the file with Alice's public key rather than private key
    signature = sign_data("public_key_file", message)
    
    print("Signature from Eve", signature, "\n")
    verify_signature = verify_sign("public_key_file", signature, message)
    if verify_signature:
        print("Bob successfully verified the signature from Eve")
    else:
        print("Bob could not verify the integrity of the message")
except:
    print("the message cannot be signed")


