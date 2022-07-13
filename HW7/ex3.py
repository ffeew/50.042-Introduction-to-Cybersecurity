from Crypto.PublicKey import RSA

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

def square_multiply(a, x, n):
    out = 1
    for i in bin(x)[2:]:
        out = out**2 % n
        if i == "1":
            out = (a * out) % n
    return out

integer = 100
s = 2
y = square_multiply(integer, public_key_e, public_key_n)
ys = square_multiply(s, public_key_e, public_key_n)
new_y = y * ys

decrypted_message = square_multiply(new_y, private_key_d,private_key_n)

print("Part II-------------")
print(f"Encrypting:  {integer}")
print("Result:")
print(y)
print("Modified to:")
print(new_y)
print(f"Decrypted:   {decrypted_message}")