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

    known_bits_p, known_bits_q = padding_two_inputs(known_bits_p,known_bits_q)

    known_bits_p = known_bits_p[::-1] ## Reverse the list
    known_bits_q = known_bits_q[::-1] ## Reverse the list
    
    p_init = root_bits(known_bits_p[0], bit_length)
    q_init = root_bits(known_bits_q[0], bit_length)

    stack = [TreeNode(p_init, q_init, 0)] ## Initialize the stack with the root
    
    while stack:
        node = stack.pop()
        p, q, i = node.p_bits, node.q_bits, node.bit_pos
             
        if i == bit_length:
            if is_valid(p, q, i, N) and (bits_to_int(p) * bits_to_int(q) == N):
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

