from math import ceil, log, gcd
from rsa import generate_prime
from rsa import mod_inverse
from helpers import *

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

    def __repr__(self):
        return (f"TreeNode(p_bits={self.p_bits}, q_bits={self.q_bits}, "
                f"dp_bits={self.dp_bits}, dq_bits={self.dq_bits}, bit_pos={self.bit_pos})")

def build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq):
    """
    Build the tree and prune invalid branches using DFS to find p and q.

    :param N: The product of p and q
    :param e: The public exponent
    :param kp: Known bits of kp
    :param known_bits_dp: Known bits of dp
    :param known_bits_dq: Known bits of dq
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """
    kq = find_kq_from_kp(kp, N, e)
    if kq is None:
        return None
    
    bit_length = max(len(known_bits_dp), len(known_bits_dq))

    known_bits_dp, known_bits_dq = padding_input(known_bits_dp, known_bits_dq)
    known_bits_dp = known_bits_dp[::-1]  # Reverse the list
    known_bits_dq = known_bits_dq[::-1]  # Reverse the list
    
    dp_init = root_bits(known_bits_dp[0], bit_length)
    dq_init = root_bits(known_bits_dq[0], bit_length)
    p_init = [0] * bit_length
    q_init = [0] * bit_length

    root_node = TreeNode(p_init, q_init, dp_init, dq_init, 0)
    stack = [root_node]  # Initialize the stack with the root
    
    while stack:
        node = stack.pop()
        p_bits, q_bits, dp_bits, dq_bits, i = node.p_bits, node.q_bits, node.dp_bits, node.dq_bits, node.bit_pos
             
        if i == bit_length:
            if is_valid(p_bits, q_bits, i, N) and (bits_to_int(p_bits) * bits_to_int(q_bits) == N):
                return p_bits, q_bits, dp_bits, dq_bits, root_node, kp, kq

        elif i < bit_length:
            dp_bits = set_bit(dp_bits, i, known_bits_dp[i])
            dq_bits = set_bit(dq_bits, i, known_bits_dq[i])

            valid_children = []

            def add_child_and_prune(dp_bits, dq_bits):
                p_bits, q_bits = find_p_q_from_dp_dq(dp_bits, dq_bits, kp, kq, e, i)
                if p_bits is not None and q_bits is not None and is_valid(p_bits, q_bits, i, N):
                    child_node = TreeNode(p_bits, q_bits, dp_bits, dq_bits, i + 1)
                    valid_children.append(child_node)
                    stack.append(child_node)

            if dp_bits[i] == -1 and dq_bits[i] == -1:
                for bit_dp in [0, 1]:
                    for bit_dq in [0, 1]:
                        dp_bits_new = set_bit(dp_bits, i, bit_dp)
                        dq_bits_new = set_bit(dq_bits, i, bit_dq)
                        add_child_and_prune(dp_bits_new, dq_bits_new)
              
            elif dp_bits[i] == -1:
                for bit_dp in [0, 1]:
                    dp_bits_new = set_bit(dp_bits, i, bit_dp)
                    dq_bits_new = dq_bits
                    add_child_and_prune(dp_bits_new, dq_bits_new)
               
            elif dq_bits[i] == -1:
                for bit_dq in [0, 1]:
                    dq_bits_new = set_bit(dq_bits, i, bit_dq)
                    dp_bits_new = dp_bits
                    add_child_and_prune(dp_bits_new, dq_bits_new)
              
            else:
                add_child_and_prune(dp_bits, dq_bits)
            
            node.children = valid_children

    return None

def branch_and_prune(N, e, known_bits_dp, known_bits_dq):
    """
    Branch and prune algorithm to factorize N, knowing non-consecutive bits of the secret values p and q.

    :param N: The product of p and q
    :param e: The public exponent
    :param known_bits_dp: Known bits of dp
    :param known_bits_dq: Known bits of dq
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """
    for kp in range(1, e):  # Assuming kp ranges from 1 to e-1
        result = build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq)
        if result is not None:
           return result
    return None

def print_tree(node, level=0):
    """
    Recursively prints the tree structure given a root node.
    
    :param node: The root node of the tree.
    :param level: The current level in the tree (used for indentation).
    """
    if node is not None:
        indent = "  " * level
        print(f"{indent}{repr(node)}")
        for child in node.children:
            print_tree(child, level + 1)

print("CRT2 Pruning Example with N = 899")

# Example usage
N = 899
e = 17
known_bits_dp = [-1, 0, -1, -1, 1]
known_bits_dq = [-1, -1, -1, 0, -1]

result = branch_and_prune(N, e, known_bits_dp, known_bits_dq)




if result is None:
    print("No solution found")
else:
    p, q, dp, dq, root_node, kp, kq = result
    p = bits_to_int(p)
    q = bits_to_int(q)
    dp = bits_to_int(dp)
    dq = bits_to_int(dq)

    print_tree(root_node)

    print("Solution found:")

    print(f"Recovered p: {p}")
    print(f"Recovered q: {q}")
    print(f"Recovered dp: {dp}")
    print(f"Recovered dq: {dq}")
    print(f"Recovered kp: {kp}")
    print(f"Recovered kq: {kq}")
