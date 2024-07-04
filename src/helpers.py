from rsa import generate_prime,generate_keypair
from sympy import mod_inverse
from math import ceil, log, gcd
import random


# Helper functions for crt_pruning

def find_kq_from_kp(kp, N, e):
    """
    Find kq from kp, N, and e using modular arithmetic.

    :param kp: Integer value of kp
    :param N: Public value  N
    :param e: Public exponent e
    :return: Integer value of kq if found, otherwise None
    """
    # Calculate the left-hand side (lhs) and right-hand side (rhs) for the equation
    lhs =(kp - 1 - (kp * N) )% e
    rhs = (kp - 1) % e

    # Check if lhs is invertible under modulo e
    if (gcd(lhs, e) != 1): 
        return None
    
    # Calculate the modular inverse of lhs
    lhs_inv = mod_inverse(lhs, e)
    if lhs_inv is None:
        return None

    # Calculate kq using the modular inverse
    kq = (rhs * lhs_inv) % e
    return kq


def find_p_q_from_dp_dq(dp, dq, kp, kq, e, i):
    """
    Calculate the bits of p and q for the given bit position i.

    :param dp: The value of dp as a list of  bits
    :param dq: The value of dq as a list of bits
    :param kp: The coefficient kp
    :param kq: The coefficient kq
    :param e: The public exponent
    :param i: The bit position to consider
    :return: The bits of p and q for the given bit posnghjkhgjgition and derived from dp and dq or None if no solution exists
    """
    bit_length = len(dp)
    # convert dp, dq, to integers
    dp = bits_to_int(dp)
    dq = bits_to_int(dq)

    # Calculate the right-hand sides of the congruences
    rhs_p = ((e * dp) - 1 + kp) 
    rhs_q = ((e * dq) - 1 + kq) 

    if gcd(kp, 1 << (i + 1)) != 1 or gcd(kq, 1 << (i + 1)) != 1:
        return (None, None)
    
    # Find the inverses of kp and kq modulo 2^i
    kp_inverse = mod_inverse(kp, 1 << (i + 1))
    kq_inverse = mod_inverse(kq, 1 << (i + 1))

    # Calculate the bits of p and q
    p_bits = (kp_inverse * rhs_p) % (1 << (i + 1))
    q_bits = (kq_inverse * rhs_q) % (1 << (i + 1))

    p_bits = int_to_bits_lsb_start(p_bits,bit_length)
    q_bits = int_to_bits_lsb_start(q_bits,bit_length)

    
    return p_bits, q_bits

# Helper functions for branch_rune and crt_pruning

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

def padding_input(bits, size):
    """
    Pads the shorter array with leading zeros to match the length of the longer array.

    :param known_bits_p: p bit array
    :param known_bits_q: q bit array
    :return: padded input
    """
    size_bits = len(bits)
    if size_bits < size:
        bits = [0] * (size - size_bits) + bits
    return bits




def padding_input_lsb_end(known_bits_p, known_bits_q):
    """
    Pads the shorter array with trailing zeros to match the length of the longer array.

    :param known_bits_p: p bit array
    :param known_bits_q: q bit array
    :return: padded input
    """
    bit_length = max(len(known_bits_p), len(known_bits_q))
    
    if len(known_bits_p) < bit_length:
        known_bits_p = known_bits_p + [0] * (bit_length - len(known_bits_p))
    if len(known_bits_q) < bit_length:
        known_bits_q = known_bits_q + [0] * (bit_length - len(known_bits_q))
        
    return known_bits_p, known_bits_q



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

def int_to_bits_lsb_start(value, length=-1):
    """
    Convert an integer into a list of bit values with the least significant bit (LSB) at the start of the list.

    :param value: Integer value to be converted.
    :param length: Desired length of the resulting bit list. If -1, the length will be determined by the number of bits in the value.
    :return: List of bits representing the integer.
    """
    # Convert the integer to a binary string and then to a list of integers (bits)
    bits = [int(bit) for bit in bin(value)[:1:-1]]
    
    # If length is provided and is greater than the number of bits, pad with leading zeros
    if length != -1:
        to_add = length - len(bits)
        bits = bits + [0] * to_add
    
    return bits

def int_to_bits_lsb_end(value, length=-1):
    """
    Convert an integer into a list of bit values with the least significant bit (LSB) at the end of the list.

    :param value: Integer value to be converted.
    :param length: Desired length of the resulting bit list. If -1, the length will be determined by the number of bits in the value.
    :return: List of bits representing the integer with LSB at the end.
    """
    # Convert the integer to a binary string, reverse the string to get LSB at the end, and then convert to a list of integers (bits)
    bits = [int(bit) for bit in bin(value)[2:]]
    
    # If length is provided and is greater than the number of bits, pad with leading zeros at the start
    if length != -1:
        to_add = length - len(bits)
        bits = [0] * to_add + bits
    
    return bits

    
    
    
# Helper functions for statistics

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
    p_bits = int_to_bits_lsb_end(p)
    q_bits = int_to_bits_lsb_end(q)

    max_bits = max(len(p_bits), len(q_bits))

    # Pad p_bits and q_bits to the same length
    p_bits = padding_input(p_bits, max_bits)
    q_bits = padding_input(q_bits, max_bits)

    # Erase bits according to the reveal rate
    p_erased = erase_bits(p_bits, reveal_rate)
    q_erased = erase_bits(q_bits, reveal_rate)

    return N, p, q, p_bits, q_bits, p_erased, q_erased

def example_generator_crt_pruning(reveal_rate, bit_size, e):
    """
    Generate example dp and dq values and theyr coresponding p and q values, calculate N, and erase bits according to the reveal rate.

    :param reveal_rate: The rate at which bits are revealed (0 to 1).
    :param bit_size: The desired bitsize for p and q.
    :param e: The public exponent
    :return: Tuple of (N, dp_actual, dq_actual, dp_erased, dq_erased, p, q)
    """
    
    N, p, q, p_bits, q_bits, p_erased, q_erased = example_generator(reveal_rate,bit_size)

    phi = (p - 1) * (q - 1)
    
    while(e > (phi - 1) or gcd(e, phi) != 1):
        N, p, q, p_bits, q_bits, p_erased, q_erased = example_generator(reveal_rate,bit_size)
        phi = (p - 1) * (q - 1)



    # Find dp and dq using the modulo inverse of e
    d = mod_inverse(e, phi)
    dp = d % (p - 1)
    dq = d % (q - 1)

    # Convert dp and dq to binary lists
    dp_bits = int_to_bits_lsb_end(dp)
    dq_bits = int_to_bits_lsb_end(dq)


    # Pad dp_bits and dq_bits to the same length

    N_bits_size = ceil(log(N,2))
    dp_bits = padding_input(dp_bits, N_bits_size)
    dq_bits = padding_input(dq_bits,N_bits_size)

    # Erase bits according to the reveal rate
    dp_erased = erase_bits(dp_bits, reveal_rate)
    dq_erased = erase_bits(dq_bits, reveal_rate)






    return N, dp_bits, dq_bits, dp, dq, dp_erased, dq_erased, p, q



## Unit tests on the different functions in the helpers.py file

def test_find_kq_from_kp(kp, kq, N, e):
    """
    Check the validity of kq for a given kp, N, and e.

    :param kp: Integer value of kp
    :param kq: Integer value of kq
    :param N: Public value N
    :param e: Public exponent e
    :return: Boolean indicating whether kq is valid
    """
    left_hand_side = (kp - 1) * (kq - 1) % e
    right_hand_side = kp * kq * N % e
    return left_hand_side == right_hand_side

