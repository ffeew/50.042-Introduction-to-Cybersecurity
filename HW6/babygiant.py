# 50.042 FCS Lab 6 template
# Year 2021

import math
import primes
import dhke
import time
from matplotlib import pyplot as plt
import numpy as np


def baby_step(alpha, beta, p, fname):
    # Calculate m = ceiling(sqrt(|G|)), 
    # i.e. size of the square root of the order of the finite cyclic group G, 
    # where group order is p-1
    m = math.ceil(math.sqrt(p - 1))

    # Compute and store into a file the values of α^(xb)*β, where 0 ≤ xb < m
    with open(fname, "w") as fout:
        for xb in range(m):
            out = (primes.square_multiply(alpha, xb, p) * beta) % p
            # using comma as the delimiter
            fout.write(str(out) + "\n")

def giant_step(alpha, p, fname):
    # Compute and store into a file the values of α^(m×xg), where 0 ≤ xg < m
    m = math.ceil(math.sqrt(p - 1))
    with open(fname, "w") as fout:
        for xg in range(m):
            out = primes.square_multiply(alpha, m * xg, p)
            fout.write(str(out) + "\n")


def baby_giant(alpha, beta, p):
    baby_step(alpha, beta, p, "baby.txt")
    giant_step(alpha, p, "giant.txt")
    m = math.ceil(math.sqrt(p - 1))
    
    hash_map = {}
    # save the value of α^(xb)*β as key and xb as value
    with open("baby.txt", "r") as fin:
        i = 0
        for line in fin:
            hash_map[line] = i
            i += 1

    with open("giant.txt", "r") as fin:
        xg = 0
        for value in fin:
            # check if α^(m×xg) is in the hash_map
            if value in hash_map:
                xb = hash_map.get(value)
                return (xg * m) - xb
            xg += 1
    raise ValueError("No match found")


if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    """
    p = 17851
    alpha = 17511
    A = 2945
    B = 11844
    sharedkey = 1671
    a = baby_giant(alpha, A, p)
    b = baby_giant(alpha, B, p)
    print(b)
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print("Guess key 1:", guesskey1)
    print("Guess key 2:", guesskey2)
    print("Actual shared key :", sharedkey)

    key_len = []
    duration = []
    for i in range(16,64, 2):
        print(f"{i}-bit key")
        p, alpha = dhke.dhke_setup(i)
        a = dhke.gen_priv_key(p)
        b = dhke.gen_priv_key(p)
        A = dhke.get_pub_key(alpha,a,p)
        B = dhke.get_pub_key(alpha,b,p)
        sharedkey = dhke.get_shared_key(B,a,p)

        start = time.time()
        a=baby_giant(alpha,A,p)
        b=baby_giant(alpha,B,p)
        guesskey1=primes.square_multiply(A,b,p)
        guesskey2=primes.square_multiply(B,a,p)
        print('Guess key 1:',guesskey1)
        print('Guess key 2:',guesskey2)
        print('Actual shared key :',sharedkey)
        end = time.time()
        time_taken = end - start
        print(f"total time taken: {time_taken}" + "\n")
        key_len.append(i)
        duration.append(time_taken)
    # plt.scatter(key_len, duration)
    log_duration = [math.log2(x) for x in duration]
    # when plotting key_len against log_duration, a straight line can be seen
    plt.scatter(key_len, log_duration)
    plt.show()
    bestfit = np.polyfit(key_len, log_duration, 1)
    number_of_bits_needed = (math.log2(2592000)-bestfit[1])/bestfit[0]
    print(number_of_bits_needed)