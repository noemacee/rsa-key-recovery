from rsa import *
from math import ceil, log, gcd


## helpers for crt

def find_kq_from_kp(kp, N, e):
    lhs = kp - 1 - kp * N
    rhs = kp - 1

    if (gcd(lhs, e) != 1): # Check if lhs is invertible     
        return None
    
    lhs_inv = mod_inverse(lhs, e)
    if lhs_inv is None:
        return None

    kq = (rhs * lhs_inv) % e
    return kq

def check_kq(kp, kq, N, e):
    left_hand_side = (kp - 1) * (kq - 1) % e
    right_hand_side = kp * kq * N % e
    return left_hand_side == right_hand_side

def find_p_q_from_dp_dq(dp, dq, kp, kq, e, i):
    """
    Calculate the bits of p and q for the given bit position i.

    :param dp: The value of dp (d mod (p-1))
    :param dq: The value of dq (d mod (q-1))
    :param kp: The coefficient kp
    :param kq: The coefficient kq
    :param e: The public exponent
    :param i: The bit position to consider
    :return: The bits of p and q for the given bit position or None if no solution exists
    """

    # convert dp, dq, to integers
    dp = bits_to_int(dp)
    dq = bits_to_int(dq)

    # Calculate the right-hand sides of the congruences
    rhs_p = (e * dp - 1 + kp) % (1 << i + 1)
    rhs_q = (e * dq - 1 + kq) % (1 << i+ 1)

    if gcd(kp, 1 << i + 1) != 1 or gcd(kq, 1 << i + 1) != 1:
        return (None, None)
    
    # Find the inverses of kp and kq modulo 2^i
    kp_inverse = mod_inverse(kp, 1 << i + 1)
    kq_inverse = mod_inverse(kq, 1 << i + 1)

    # Calculate the bits of p and q
    p_bits = (kp_inverse * rhs_p) % (1 << i + 1)
    q_bits = (kq_inverse * rhs_q) % (1 << i + 1)

    p_bits = int_to_bits(p_bits)
    q_bits = int_to_bits(q_bits)

    
    return p_bits, q_bits

def verify_dp_dq(dp, dq, p, q, e):
    
    if (e * dp) % (p - 1) != 1:
        print("edp ≡ 1 mod (p-1) failed")
        print((e * dp) % (p - 1),)
        print (dp, "dp")
        return False
    if (e * dq) % (q - 1) != 1:
        print("edq ≡ 1 mod (q-1) failed")
        return False
    if p * q != N:
        print("p * q != N failed")
        return False
    return True

## general helpers



def root_bits(lsb, bit_length):
    """
    Initialize the fist value of p or q to only zeros exept for the least significant bit

    :param lsb: least significant bit
    :param bit_length: The total length of the bit sequence.
    :return: A list of bits where all bits are zero exept for the lsb
    """
    bits = [0] * bit_length  # Initialize all bits to 0
    bits[0] = lsb
    return bits

def padding_input(known_bits_p, known_bits_q):
    """
    Pads the shorter array with leading zeros to match the length of the longer array.

    :param known_bits_p: p bit array
    :param known_bits_q: q bit array
    :return: padded input
    """
    bit_length = max(len(known_bits_p), len(known_bits_q))
    
    if len(known_bits_p) < bit_length:
        known_bits_p = [0] * (bit_length - len(known_bits_p)) + known_bits_p
    if len(known_bits_q) < bit_length:
        known_bits_q = [0] * (bit_length - len(known_bits_q)) + known_bits_q
    return known_bits_p,known_bits_q


def is_valid(p_bits, q_bits, i, N):
    """
    Check if the current bit configuration of p_bits and q_bits is valid according to the integer relation N mod 2^i = p*q mod 2^i.

    :param p_bits: Bits of p
    :param q_bits: Bits of q
    :param i: Current bit position
    :param N: Public key to be factorized
    :return: True if valid, False otherwise
    """
    p_bits = bits_to_int(p_bits)
    q_bits = bits_to_int(q_bits)

    return (p_bits * q_bits) % (1 << (i + 1)) == N % (1 << (i + 1))


def set_bit(bits, bit_pos, value):
    """
    Set the bit at the specified position to the given value.

    :param bits: List of bit values
    :param bit_pos: Position to set the bit
    :param value: Value to set (0 or 1)
    :return: New list of bits with the updated value
    """
    new_bits = bits[:]
    new_bits[bit_pos] = value
    return new_bits

def bits_to_int(bits):
    """
    Convert a list of bit values (0 or 1) to an integer.

    :param bits: List of bit values (0 or 1).
    :return: Integer value of the bit sequence.
    """
    value = 0
    for bit in bits[::-1]:
        value = (value << 1) | bit
    return value

def int_to_bits(value):
    """
    Convert an integer into a list of bit values

    :param value: Integer value
    :return: List of bits
    """
    return [int(bit) for bit in bin(value)[2:]]
    
## helpers for statistics

def erase_bits(bits, revealrate):
    """
    Erase bits according to the reveal rate by setting them to -1.

    :param bits: List of bits.
    :param revealrate: The rate at which bits are revealed (0 to 1).
    :return: List of bits with some bits erased.
    """
    return [bit if random.random() < revealrate else -1 for bit in bits]    


def example_generator(reveal_rate, bit_size):
    """
    Generate example p and q values, calculate N, and erase bits according to the reveal rate.

    :param reveal_rate: The rate at which bits are revealed (0 to 1).
    :param bit_size: The desired bitsize for p and q.
    :return: Tuple of (N, p_actual, q_actual, p_erased, q_erased)
    """
    # Generate p and q
    p = generate_prime(bit_size)
    q = generate_prime(bit_size)

    # Calculate N
    N = p * q

    # Convert p and q to binary lists
    p_bits = int_to_bits(p)
    q_bits = int_to_bits(q)

    # Pad p_bits and q_bits to the same length
    p_bits, q_bits = padding_input(p_bits, q_bits)

    # Erase bits according to the reveal rate
    p_erased = erase_bits(p_bits, reveal_rate)
    q_erased = erase_bits(q_bits, reveal_rate)

    return N,p,q, p_bits, q_bits, p_erased, q_erased
