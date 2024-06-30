import random
from math import gcd


# Function to test if a number is prime using Miller-Rabin primality test




def miller_rabin(n, k=128):
    """
    Test if an integer n is a prime number using Miller-Rabin primality test. The parameter k is the number of tests to perform. The higher the value of k, the more accurate the test.
    
    n: int - the number to test for primality
    k: int - the number of tests to perform

    output: bool - True if n is prime, False otherwise
    """
    
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
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

# Function to generate a prime number of specified bit length

def generate_prime(bits):
    """ 
    Generate a prime number of specified bit length. 
    
    bits: int - the bit length of the prime number to generate

    output: int - a prime number of the specified bit length
    """
    while True:
        p = random.getrandbits(bits)
        if p % 2 == 0:
            continue
        if miller_rabin(p):
            return p

def gcd(a, b):
    """ 
    Compute the greatest common divisor using Euclid's algorithm. 
    
    a: int - the first number
    b: int - the second number

    output: int - the greatest common divisor of a and b
    """
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """ 
    Compute the modular inverse of a modulo m. The euclidean algorithm is used for its numerical efficiency and stability.
    
    a: int - the number to compute the inverse of
    m: int - the modulus

    output: int - the modular inverse of a modulo m
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1



def generate_keypair(bits):
    """ 
    Generate RSA key pair. 
    
    bits: int - the bit length of the prime numbers to generate

    output: tuple - the public key (e, n) and the private key (p, q, phi, d)
    """
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # commonly used prime exponent
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)
    public_key = (e, n)
    private_key = (p, q, phi, d)
    return public_key, private_key

def encrypt(public_key, plaintext):
    # Use the CRT to speed up the encryption

def decrypt(private_key, ciphertext):
    # Use the CRT to speed up the decryption