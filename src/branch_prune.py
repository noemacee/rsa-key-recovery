from math import ceil, log
from rsa import generate_prime
import random
from helpers import *



class TreeNode:
    def __init__(self, p_bits, q_bits, bit_pos):
        self.p_bits = p_bits
        self.q_bits = q_bits
        self.bit_pos = bit_pos
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


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

    known_bits_p, known_bits_q = padding_input(known_bits_p,known_bits_q)

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
print("Example 1 with N = 899 \n")
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
print("Example 2 with N = 2'053'351 \n")
    
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


# Example 3 usage of example_generator
print("\n Example 3 using example_generator \n")

revealrate = 0.5
bitsize = 6  # Use a small bitsize for demonstration purposes

N,p,q, p_actual, q_actual, p_erased, q_erased = example_generator(revealrate, bitsize)

print(f"N: {N}")
print(f"p_actual: {p_actual}")
print(f"p as int: {p}")

print(f"q_actual: {q_actual}")
print(f"q as int: {q}")

print(f"p_erased: {p_erased}")
print(f"q_erased: {q_erased}")

# Find the factors p and q
result = branch_and_prune(N, p_erased, q_erased)

if result is None : 
    print("No solution found")
else:
    p, q = result
    print(f"Recovered p: {p[::-1]}")
    print(f"Recovered q: {q[::-1]}")
    print(f"p as int: {bits_to_int(p)}")
    print(f"q as int: {bits_to_int(q)}")

