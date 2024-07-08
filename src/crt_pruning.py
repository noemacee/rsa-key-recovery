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
            if  verify_integer_relations(dp_bits,dq_bits,p_bits,q_bits,e,N,kp,kq):
                return p_bits, q_bits, dp_bits, dq_bits, root_node, kp, kq

        elif i < bit_length:    
            dp_bits = set_bit(dp_bits, i, known_bits_dp[i])
            dq_bits = set_bit(dq_bits, i, known_bits_dq[i])

            valid_children = []

            def add_child_and_prune(dp_bits, dq_bits, p_bits, q_bits):               
                dp = bits_to_int(dp_bits)
                dq = bits_to_int(dq_bits)

                lhs_p = (((e*dp) - 1 + kp) % (1 << (i + 1)))
                lhs_q = (((e*dq) - 1 + kq) % (1 << (i + 1)))

                for p_bit_i in [0, 1] : 
                    for q_bit_i in [0, 1] : 
                        p_bits = set_bit(p_bits, i, p_bit_i)
                        q_bits = set_bit(q_bits, i, q_bit_i)
                        bol1 = (((bits_to_int(p_bits) * kp )%  (1 << (i + 1))) == lhs_p)
                        bol2 = (((bits_to_int(q_bits) * kq)%  (1 << (i + 1))) == lhs_q)
                        bol3 = is_valid(p_bits, q_bits, i, N)

                        if (bol1 and bol2 and bol3) : 
                            child_node = TreeNode(p_bits, q_bits, dp_bits, dq_bits, i + 1)
                            valid_children.append(child_node)
                            stack.append(child_node)
                    

            if dp_bits[i] == -1 and dq_bits[i] == -1:
                for bit_dp in [0, 1]:
                    for bit_dq in [0, 1]:
                        dp_bits_new = set_bit(dp_bits, i, bit_dp)
                        dq_bits_new = set_bit(dq_bits, i, bit_dq)
                        add_child_and_prune(dp_bits_new, dq_bits_new, p_bits, q_bits)
              
            elif dp_bits[i] == -1:
                for bit_dp in [0, 1]:
                    dp_bits_new = set_bit(dp_bits, i, bit_dp)
                    dq_bits_new = dq_bits
                    add_child_and_prune(dp_bits_new, dq_bits_new, p_bits, q_bits)
               
            elif dq_bits[i] == -1:
                for bit_dq in [0, 1]:
                    dq_bits_new = set_bit(dq_bits, i, bit_dq)
                    dp_bits_new = dp_bits
                    add_child_and_prune(dp_bits_new, dq_bits_new, p_bits, q_bits)
              
            else:
                add_child_and_prune(dp_bits, dq_bits, p_bits, q_bits)
            
            node.children = valid_children
    return None

def branch_and_prune_crt(N, e, known_bits_dp, known_bits_dq):
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

