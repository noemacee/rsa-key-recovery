from math import ceil, log

class TreeNode:
    def __init__(self, p_bits, q_bits, bit_pos):
        self.p_bits = p_bits
        self.q_bits = q_bits
        self.bit_pos = bit_pos
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


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


def build_tree_and_prune_dfs(N, known_bits_p, known_bits_q):
    """
    Build the tree and prune invalid branches using DFS to find p and q.

    :param N: The product of p and q
    :param known_bits_p: Known bits of p
    :param known_bits_q: Known bits of q
    :param bit_length: Length of the bit sequences
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """
    bit_length = max(len(known_bits_p), len(known_bits_q))

    # Pads the shorter array with leading zeros to match the length of the longer array.
    if len(known_bits_p) < bit_length:
        known_bits_p = [0] * (bit_length - len(known_bits_p)) + known_bits_p
    if len(known_bits_q) < bit_length:
        known_bits_q = [0] * (bit_length - len(known_bits_q)) + known_bits_q


    known_bits_p = known_bits_p[::-1] ## Reverse the list
    known_bits_q = known_bits_q[::-1] ## Reverse the list
    
    p_init = root_bits(known_bits_p[0], bit_length)
    q_init = root_bits(known_bits_q[0], bit_length)

    stack = [TreeNode(p_init, q_init, 0)] ## Initialize the stack with the root
    
    while stack:
        node = stack.pop()
        p, q, i = node.p_bits, node.q_bits, node.bit_pos
             
        if i == bit_length:
            if is_valid(p, q, i, N):
                return p, q

        elif i < bit_length:
            p = set_bit(p, i, known_bits_p[i])
            q = set_bit(q, i, known_bits_q[i])

            valid_children = []

            def add_child_and_prune(p_bits, q_bits):
                if is_valid(p_bits, q_bits, i, N):
                    child_node = TreeNode(p_bits, q_bits, i + 1)
                    valid_children.append(child_node)
                    stack.append(child_node)

            if p[i] == -1 and q[i] == -1:
                for bit_p in [0, 1]:
                    for bit_q in [0, 1]:
                        p_bits_new = set_bit(p, i, bit_p)
                        q_bits_new = set_bit(q, i, bit_q)
                        add_child_and_prune(p_bits_new, q_bits_new)
              
            elif p[i] == -1:
                for bit_p in [0, 1]:
                    p_bits_new = set_bit(p, i, bit_p)
                    q_bits_new = q
                    add_child_and_prune(p_bits_new, q_bits_new)
               
            elif q[i] == -1:
                for bit_q in [0, 1]:
                    q_bits_new = set_bit(q, i, bit_q)
                    p_bits_new = p
                    add_child_and_prune(p_bits_new, q_bits_new)
              
            else:
                add_child_and_prune(p, q)
            

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
    return build_tree_and_prune_dfs(N, known_bits_p, known_bits_q)


# Example usage 1
N = 899
known_bits_p = [-1,1,1,-1,1]
known_bits_q = [-1,1,-1,0,-1]


# Find the factors p and q
result = branch_and_prune(N, known_bits_p, known_bits_q)

if result is None : 
    print("No solution found")
else:
    p, q = result
    print(f"Recovered p: {p[::-1]}")
    print(f"Recovered q: {q[::-1]}")
    print(f"p as int: {bits_to_int(p)}")
    print(f"q as int: {bits_to_int(q)}")

# Example usage 2
N = 2053351

# p is 1013: [1,1,1,1,1,1,0,1,0,1]
known_bits_p = [1,-1,1,1,-1,-1,0,-1,-1,1]

# q is 2027: [1,1,1,1,1,1,0,1,0,1,1]
known_bits_q = [1,1,-1,1,1,-1,0,-1,-1,1,-1]


# Find the factors p and q
result = branch_and_prune(N, known_bits_p, known_bits_q)

if result is None : 
    print("No solution found")
else:
    p, q = result
    print(f"Recovered p: {p[::-1]}")
    print(f"Recovered q: {q[::-1]}")
    print(f"p as int: {bits_to_int(p)}")
    print(f"q as int: {bits_to_int(q)}")


# Optional: write a function that produces examples with a given erasure rate, bit sice for p and q and use it to calculate statistics on how long it takes to factor given an errorrate




