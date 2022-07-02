# 50.042 FCS Lab 6 template
# Year 2021

import primes
import random
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# def generate_primitive_element(p):
#     a = random.randint(2, p-2)

#     not_primitive = True
#     while not_primitive:
#         # check if a^(p-1) mod p == 1, 
#         # if not, it is not a primitive element
#         print('trying: ', a)
#         if pow(a, p-1, p) !=1:
#             a = random.randint(2, p-2)
#         else:
#             # check if there is any powers of a before p-1 that
#             # satisfies a^(i-1) mod p == 1, if yes, a is not primitive
#             not_primitive = False
#             for i in range(1,p):
#                 test = pow(a, i, p)
#                 print(test)
#                 if (test == 1) and (i != p-1):
#                     a = random.randint(2, p-2)
#                     not_primitive = True
#                     break
                    
#     return a 
    

def dhke_setup(nb):
    p = primes.gen_prime_nbits(nb)
    # a = generate_primitive_element(p)
    a = random.randint(2, p-2)
    return p, a


def gen_priv_key(p):
    return random.randint(2, p-2)


def get_pub_key(alpha, a, p):
    return primes.square_multiply(alpha,a,p)


def get_shared_key(keypub, keypriv, p):
    return primes.square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    p, alpha = dhke_setup(256)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())
    print()
    
    # generate a 256 bit key for AES encryption
    while True:
        p, alpha = dhke_setup(256)
        a = gen_priv_key(p)
        b = gen_priv_key(p)
        A = get_pub_key(alpha, a, p)
        B = get_pub_key(alpha, b, p)
        sharedKeyA = get_shared_key(B, a, p)
        sharedKeyB = get_shared_key(A, b, p)
        if sharedKeyA.bit_length() == 256:
            break

    print("#### Demonstration of Diffie-Hellman Key Exchange ####")
    print('Shared key A = ', sharedKeyA)
    print('Shared key B = ', sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())
    print()

    def encrypt(key, plaintext, associated_data):
        # Generate a random 96-bit IV.
        iv = os.urandom(12)

        encryptor = Cipher(algorithms.AES(key),modes.GCM(iv),).encryptor()

        # associated_data will be authenticated but not encrypted,
        # it must also be passed in on decryption.
        encryptor.authenticate_additional_data(associated_data)

        # Encrypt the plaintext and get the associated ciphertext.
        # GCM does not require padding.
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return (iv, ciphertext, encryptor.tag)

    def decrypt(key, associated_data, iv, ciphertext, tag):
        # Construct a Cipher object, with the key, iv, and additionally the
        # GCM tag used for authenticating the message.
        decryptor = Cipher(algorithms.AES(key),modes.GCM(iv, tag),).decryptor()

        # We put associated_data back in or the tag will fail to verify
        # when we finalize the decryptor.
        decryptor.authenticate_additional_data(associated_data)

        # Decryption gets us the authenticated plaintext.
        # If the tag does not match an InvalidTag exception will be raised.
        return decryptor.update(ciphertext) + decryptor.finalize()

    plaintext = b"This is a secret message"

    print("Plaintext sent by A: ", plaintext)

    iv, ciphertext, tag = encrypt(sharedKeyA.to_bytes(32,'big'), plaintext, b"authenticated but not encrypted payload")
    print("Ciphertext sent by A: ", ciphertext)

    decrypted_msg = decrypt(sharedKeyB.to_bytes(32,'big'), b"authenticated but not encrypted payload", iv, ciphertext, tag)
    print("Decrypted plaintext by B: ", decrypted_msg)