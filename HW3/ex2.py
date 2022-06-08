import string
import hashlib
import time

# function takes in a hash and returns a value that will result in the hash
def brute_force_collision(hash):
    alphabet = string.ascii_lowercase + string.digits
    for letter1 in alphabet:
        for letter2 in alphabet:
            for letter3 in alphabet:
                for letter4 in alphabet:
                    for letter5 in alphabet:
                        plaintext = letter1 + letter2 + letter3 + letter4 + letter5
                        hashed_value = hashlib.md5(plaintext.encode())
                        if hashed_value.hexdigest() == hash:
                            return plaintext
    return "Error"

start = time.time()
print("Start")

fout = open("ex2_hash.txt", mode = "w")

with open("hash5.txt") as fin:
    answers = []
    for hash in fin:
        answer = brute_force_collision(hash.strip())
        print(answer)
        answers.append(answer)
    fout.writelines([ans +"\n" for ans in answers])
    print(answers)

end = time.time()
print(end)
print(f"Elapsed time: {end - start}")