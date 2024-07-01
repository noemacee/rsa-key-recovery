from math import ceil, log

class TreeNode:
    def __init__(self, p_bits, q_bits, bit_pos):
        self.p_bits = p_bits
        self.q_bits = q_bits
        self.bit_pos = bit_pos
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def initialize_bits(known_bit, bit_length):
    """
    Initialize the bit sequence with known and unknown bits.

    :param known_bits: A string representing known ('0' or '1') and unknown ('?') bits.
    :param bit_length: The total length of the bit sequence.
    :return: A list of integers where known bits are represented by 0 or 1 and unknown bits by -1.
    """
    bits = [0] * bit_length  # Initialize all bits to -1
    if known_bit != -1:
        bits[0] = int(known_bit)
    return bits


def is_valid(p_bits, q_bits, i, N):
    return (p_bits * q_bits) % (1 << (i + 1)) == N % (1 << (i + 1))


def set_bit(bits, bit_pos, value):
    new_bits = bits[:]
    new_bits[bit_pos] = value
    return new_bits


def build_tree_and_prune_dfs(N, known_bits_p, known_bits_q, bit_length):
    p_init = initialize_bits(known_bits_p[0], bit_length)
    q_init = initialize_bits(known_bits_q[0], bit_length)

    stack = []
    root = TreeNode(p_init, q_init, 0)

    stack.append(root)
    
    while stack:
        node = stack.pop()
        i = node.bit_pos

        if i == bit_length + 1: ## DNF
            continue

        valid_children = []

        def add_child_and_prune(p_bits, q_bits):
            if is_valid(p_bits, q_bits, i, N):
                child_node = TreeNode(p_bits, q_bits, i + 1)
                valid_children.append(child_node)
                stack.append(child_node)

        if node.p_bits[i] == -1 and node.q_bits[i] == -1:
            for bit_p in [0, 1]:
                for bit_q in [0, 1]:
                    p_bits_new = set_bit(node.p_bits, i, bit_p)
                    q_bits_new = set_bit(node.q_bits, i, bit_q)
                    add_child_and_prune(p_bits_new, q_bits_new)
        elif node.p_bits[i] == -1:
            for bit_p in [0, 1]:
                p_bits_new = set_bit(node.p_bits, i, bit_p)
                q_bits_new = node.q_bits
                add_child_and_prune(p_bits_new, q_bits_new)
        elif node.q_bits[i] == -1:
            for bit_q in [0, 1]:
                q_bits_new = set_bit(node.q_bits, i, bit_q)
                p_bits_new = node.p_bits
                add_child_and_prune(p_bits_new, q_bits_new)
        else:
            p_bits_new = node.p_bits
            q_bits_new = node.q_bits
            add_child_and_prune(p_bits_new, q_bits_new)

        node.children = valid_children

    return root


def find_solutions(node, solutions, N, bit_length):
    if node.bit_pos == bit_length:
        p = node.p_bits
        q = node.q_bits

        if p * q == N:
            solutions.append((p, q))
        return

    for child in node.children:
        find_solutions(child, solutions, N, bit_length)


def branch_and_prune(N, known_bits_p, known_bits_q, bit_length):
    root = build_tree_and_prune_dfs(N, known_bits_p, known_bits_q, bit_length)
    solutions = []
    find_solutions(root, solutions, N, bit_length)
    return solutions


def print_tree(node, bit_length, indent=""):
    if node.bit_pos == bit_length:
        p = int("".join(['0' if bit == -1 else str(bit) for bit in node.p_bits[::-1]]), 2)
        q = int("".join(['0' if bit == -1 else str(bit) for bit in node.q_bits[::-1]]), 2)
        print(f"{indent}Node: p={p}, q={q}")
        return
    p_bits_str = "".join(['?' if bit == -1 else str(bit) for bit in node.p_bits[::-1]])
    q_bits_str = "".join(['?' if bit == -1 else str(bit) for bit in node.q_bits[::-1]])
    print(f"{indent}Node: p_bits={p_bits_str}, q_bits={q_bits_str}, bit_pos={node.bit_pos}")
    for child in node.children:
        print_tree(child, bit_length, indent + "  ")


# Example usage
N = 899
known_bits_p = [-1,1,1,-1,1]
known_bits_q = [-1,1,-1,0,-1]

# Calculate the bit length of the factors
bit_length = max(len(known_bits_p), len(known_bits_q))




solutions = branch_and_prune(N, known_bits_p, known_bits_q, bit_length)
for p, q in solutions:
    print(f"Recovered p: {p}")
    print(f"Recovered q: {q}")

# Optional: Print the tree structure for debugging
root = build_tree_and_prune_dfs(N, known_bits_p, known_bits_q, bit_length)
print_tree(root, bit_length)
