# 50.042 FCS Lab 6 template
# Year 2021

import random

def square_multiply(a, x, n):
    out = 1
    for i in bin(x)[2:]:
        out = out**2 % n
        if i == "1":
            out = (a * out) % n
    return out

# credits to: https://gist.github.com/Ayrx/5884790
def miller_rabin(n, a):

    if n == 2 or n==3:
        return True

    # composite number if n is even
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(a):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# credits to: https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
def generate_prime_candidate(length):
    # generate random bits
    p = random.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def gen_prime_nbits(n):
    p = 4
    # keep generating while the primality test fail
    while not miller_rabin(p, 40):
        p = generate_prime_candidate(n)
    return p

if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561,2))
    print('Is 27 a prime?')
    print(miller_rabin(27,2))
    print('Is 61 a prime?')
    print(miller_rabin(61,2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))
