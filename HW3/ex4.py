import random
import string
import hashlib

lowercase = string.ascii_lowercase

fout_hashes = open("salted6.txt", mode = "w")
fout_plaintexts = open("plain6.txt", mode = "w")

with open("ex2_hash.txt") as fin:
    hashes = []
    plaintexts = []
    for plaintext in fin:
        print(plaintext)
        salted_plaintext = plaintext.strip()+lowercase[random.randint(0,len(lowercase)-1)]
        plaintexts.append(salted_plaintext)
        salted_hash = hashlib.md5(salted_plaintext.encode()).hexdigest()
        hashes.append(salted_hash)
    fout_hashes.writelines([hash +"\n" for hash in hashes])
    fout_plaintexts.writelines([plaintext +"\n" for plaintext in plaintexts])
    print(hashes)
