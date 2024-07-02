from math import ceil, log, gcd
from rsa import generate_prime
import random
from sympy import mod_inverse



class TreeNode:
    def __init__(self, p_bits, q_bits, dp_bits, dq_bits, bit_pos):
        self.p_bits = p_bits
        self.q_bits = q_bits
        self.dp_bits = dp_bits
        self.dq_bits = dq_bits
        self.bit_pos = bit_pos
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


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


def build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq):
    """
    Build the tree and prune invalid branches using DFS to find p and q.

    :param N: The product of p and q
    :param known_bits_p: Known bits of p
    :param known_bits_q: Known bits of q
    :param bit_length: Length of the bit sequences
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """
    bit_length = max(len(known_bits_dp), len(known_bits_dq))

    known_bits_dp, known_bits_dq = padding_input(known_bits_dp,known_bits_dq)

    known_bits_dp = known_bits_dp[::-1] ## Reverse the list
    known_bits_dq = known_bits_dq[::-1] ## Reverse the list
    
    dp_init = root_bits(known_bits_dp[0], bit_length)
    dq_init = root_bits(known_bits_dq[0], bit_length)
    p_init = [0] * bit_length
    q_init = [0] * bit_length

    stack = [TreeNode(p_init,q_init,dp_init, dq_init, 0)] ## Initialize the stack with the root
    
    while stack:
        node = stack.pop()
        p, q, dp, dq, i = node.p_bits, node.q_bits, node.dp_bits, node.dq_bits, node.bit_pos
             
        if i == bit_length:
            if is_valid(p, q, i, N):
                return p, q, dp, dq

        elif i < bit_length:
            dp = set_bit(p, i, known_bits_dp[i])
            dq = set_bit(q, i, known_bits_dq[i])

            valid_children = []

            def add_child_and_prune(dp_bits, dq_bits):
                p_bits = get_p_from_dp(dp_bits)
                q_bits = get_q_from_dq(dq_bits)
                if is_valid(p_bits, q_bits, i, N):
                    child_node = TreeNode(p_bits, q_bits, dp_bits, dq_bits, i + 1)
                    valid_children.append(child_node)
                    stack.append(child_node)

            if dp[i] == -1 and dq[i] == -1:
                for bit_dp in [0, 1]:
                    for bit_dq in [0, 1]:
                        dp_bits_new = set_bit(dp, i, bit_dp)
                        dq_bits_new = set_bit(dq, i, bit_dq)
                        add_child_and_prune(dp_bits_new, dq_bits_new)
              
            elif dp[i] == -1:
                for bit_dp in [0, 1]:
                    dp_bits_new = set_bit(dp, i, bit_dp)
                    dq_bits_new = dq
                    add_child_and_prune(dp_bits_new, dq_bits_new)
               
            elif dq[i] == -1:
                for bit_dq in [0, 1]:
                    dq_bits_new = set_bit(q, i, bit_dq)
                    dp_bits_new = p
                    add_child_and_prune(dp_bits_new, dq_bits_new)
              
            else:
                add_child_and_prune(dp, dq)
            

            node.children = valid_children
         

    return None

def branch_and_prune(N, known_bits_p, known_bits_q):
    """
    Branch and prune algorithm to factorize N, knowing non-consecutive bits of the secret values p and q

    :param N: The product of p and q
    :param known_bits_p: Known bits of p
    :param known_bits_q: Known bits of q
    :param bit_length: Length of the bit sequences of p and q
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """

    for kp in range(1, e):  # Assuming kp ranges from 1 to e-1
        result = build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq)
        if result is not None:
        ##    if verify_dp_dq(bits_to_int(result[0]), bits_to_int(result[1]), 29, 31, e):
            return result
    return None
    


# Example usage
N = 899
e = 17
known_bits_dp = [-1, 0, -1, -1, 1]
known_bits_dq = [-1, -1, -1, 0, -1]




result = branch_and_prune(N, e, known_bits_dp, known_bits_dq)

if result is None:
    print("No solution found")
else:
    dp, dq = result
    dp_int = bits_to_int(dp)
    dq_int = bits_to_int(dq)
    p_int = 29
    q_int = 31

    if verify_dp_dq(dp_int, dq_int, p_int, q_int, e):
        print("The solution is coherent.")
    else:
        print("The solution is not coherent.")

    print(f"Recovered dp: {dp[::-1]}")
    print(f"Recovered dq: {dq[::-1]}")
    print(f"dp as int: {bits_to_int(dp)}")
    print(f"dq as int: {bits_to_int(dq)}")
