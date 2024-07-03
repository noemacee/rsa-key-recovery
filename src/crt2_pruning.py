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
    :param known_bits_p: Known bits of p
    :param known_bits_q: Known bits of q
    :param bit_length: Length of the bit sequences
    :return: Tuple of bit sequences for p and q if found, None otherwise
    """
    
    kq = find_kq_from_kp(kp, N, e)
    if kq is None:
        print("kq was not found")
        return None
    print(check_kq(kp,kq,N,e))
    
    bit_length = max(len(known_bits_dp), len(known_bits_dq))

    known_bits_dp, known_bits_dq = padding_input(known_bits_dp,known_bits_dq)

    known_bits_dp = known_bits_dp[::-1] ## Reverse the list
    known_bits_dq = known_bits_dq[::-1] ## Reverse the list
    
    dp_init = root_bits(known_bits_dp[0], bit_length)
    dq_init = root_bits(known_bits_dq[0], bit_length)
    p_init = [0] * bit_length
    q_init = [0] * bit_length

    root_node = TreeNode(p_init,q_init,dp_init, dq_init, 0)
    stack = [root_node] ## Initialize the stack with the root
    
    while stack:
        node = stack.pop()
        p, q, dp, dq, i = node.p_bits, node.q_bits, node.dp_bits, node.dq_bits, node.bit_pos
             
        if i == bit_length:
            print("we reached i == bitlength")
            if is_valid(p, q, i, N):
                return p, q, dp, dq, root_node

        elif i < bit_length:
            dp = set_bit(dp, i, known_bits_dp[i])
            dq = set_bit(dq, i, known_bits_dq[i])

            valid_children = []

            def add_child_and_prune(dp_bits, dq_bits):
    
                p_bits,q_bits = find_p_q_from_dp_dq(dp_bits, dq_bits, kp, kq, e, i)
                ##print("we are trying to add the child with:")

                ##print(f"p_bits: {p_bits}")
                ##print(f"q_bits: {q_bits}")

                if p_bits is not None and q_bits is not None and is_valid(p_bits, q_bits, i, N):
                    print("child adding")
                    print(f"p_bits: {p_bits}")
                    print(f"q_bits: {q_bits}")
                    print(f"dp: {dp_bits}")
                    print(f"dq: {dq_bits}")


                    child_node = TreeNode(p_bits, q_bits, dp_bits, dq_bits, i + 1)
                    valid_children.append(child_node)
                    stack.append(child_node)

            if dp[i] == -1 and dq[i] == -1:
                print("both dp and dq are unknown")
                for bit_dp in [0, 1]:
                    for bit_dq in [0, 1]:
                        dp_bits_new = set_bit(dp, i, bit_dp)
                        dq_bits_new = set_bit(dq, i, bit_dq)
                        add_child_and_prune(dp_bits_new, dq_bits_new)
              
            elif dp[i] == -1:
                print("dp is unknown")
                for bit_dp in [0, 1]:
                    dp_bits_new = set_bit(dp, i, bit_dp)
                    dq_bits_new = dq
                    add_child_and_prune(dp_bits_new, dq_bits_new)
               
            elif dq[i] == -1:
                print("dq is unknown")
                for bit_dq in [0, 1]:
                    dq_bits_new = set_bit(dq, i, bit_dq)
                    dp_bits_new = dp
                    add_child_and_prune(dp_bits_new, dq_bits_new)
              
            else:
                print("both are known")
                add_child_and_prune(dp, dq)
            

            node.children = valid_children
         

    return None

def branch_and_prune(N, e, known_bits_p, known_bits_q):
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
    

def print_tree(node, level=0):
    """
    Recursively prints the tree structure given a root node.
    
    :param node: The root node of the tree.
    :param level: The current level in the tree (used for indentation).
    """
    if node is not None:
        # Print the current node with indentation based on the level
        indent = "  " * level
        print(f"{indent}{repr(node)}")
        
        # Recursively print all children
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
    p, q, dp, dq, root_node = result
    p = bits_to_int(p)
    q = bits_to_int(q)
    dp = bits_to_int(dp)
    dq = bits_to_int(dq)

    print_tree(root_node)

    print(f"Recovered p: {p}")
    print(f"Recovered q: {q}")
    print(f"Recovered dp: {dp}")
    print(f"Recovered dq: {dq}")



