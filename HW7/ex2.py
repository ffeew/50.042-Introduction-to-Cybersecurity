from Crypto.PublicKey import RSA
import math
from Crypto.Hash import SHA256

def square_multiply(a, x, n):
    out = 1
    for i in bin(x)[2:]:
        out = out**2 % n
        if i == "1":
            out = (a * out) % n
    return out

public_key = open('mykey.pem.pub','r').read()
rsakey = RSA.importKey(public_key)
# public key
public_key_n = rsakey.n
public_key_e = rsakey.e

private_key = open('mykey.pem.priv','r').read()
rsakey = RSA.importKey(private_key)
# private key
private_key_n = rsakey.n
private_key_d = rsakey.d

# credits to https://stackoverflow.com/questions/44504397/generate-an-integer-for-encryption-from-a-string-and-vice-versa
def string_to_int(s):
    return int.from_bytes(s.encode(), byteorder='little')

def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little').decode()


def encrypt(message, e, n):
    message_int = string_to_int(message)
    encrypted_msg = square_multiply(message_int, e, n)
    return encrypted_msg

def decrypt(cipher, d, n):
    decrypted_msg_int = square_multiply(cipher, d, n)
    decrypted_message = int_to_string(decrypted_msg_int)
    return decrypted_message

message = open('message.txt','r').read()
a = encrypt(message, public_key_e, public_key_n)
print("encrypted message = ", a, "\n")

b = decrypt(a, private_key_d, private_key_n)
print("decrypted message = ", b, "\n")

# check if message is the same after encryption and decryption
assert b == message

print("\n =============== Checking Message Signature ================ \n")
message_in_bytes = message.encode()

message_hash = SHA256.new(message_in_bytes)

print("SHA256 hash of message = ", message_hash.hexdigest(), "\n")

message_hash_int = int.from_bytes(message_hash.digest(), byteorder="little")

print("SHA256 hash of message using integer representation = ", message_hash_int, "\n")

private_signature = square_multiply(message_hash_int, private_key_d, private_key_n)

print("private signature = ", private_signature, "\n")

signature_verification = square_multiply(private_signature, public_key_e, public_key_n)

print("signature_verification = ", signature_verification, "\n")

# check if the final hash is the same as the hash value of the plaintext
assert signature_verification==message_hash_int