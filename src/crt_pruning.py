from math import ceil, log, gcd
from sympy import mod_inverse


class TreeNode:
    def __init__(self, dp_bits, dq_bits, bit_pos):
        self.dp_bits = dp_bits
        self.dq_bits = dq_bits
        self.bit_pos = bit_pos
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

def root_bits(lsb, bit_length):
    bits = [0] * bit_length
    bits[0] = lsb
    return bits

def is_valid(dp_bits, dq_bits, i, N):
    dp = bits_to_int(dp_bits)
    dq = bits_to_int(dq_bits)
    result = (dp * dq) % (1 << (i + 1)) == N % (1 << (i + 1))
    return result

def set_bit(bits, bit_pos, value):
    new_bits = bits[:]
    new_bits[bit_pos] = value
    return new_bits

def bits_to_int(bits):
    value = 0
    for bit in bits[::-1]:
        value = (value << 1) | bit
    return value

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

def build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq):
    kq = find_kq_from_kp(kp, N, e)
    
    if kq is None:
        return None


    bit_length = max(len(known_bits_dp), len(known_bits_dq))

    if len(known_bits_dp) < bit_length:
        known_bits_dp = [0] * (bit_length - len(known_bits_dp)) + known_bits_dp
    if len(known_bits_dq) < bit_length:
        known_bits_dq = [0] * (bit_length - len(known_bits_dq)) + known_bits_dq

    known_bits_dp = known_bits_dp[::-1]
    known_bits_dq = known_bits_dq[::-1]

    dp_init = root_bits(known_bits_dp[0], bit_length)
    dq_init = root_bits(known_bits_dq[0], bit_length)
    print(dp_init[0], dq_init[0])

    stack = [TreeNode(dp_init, dq_init, 0)]

    while stack:
        node = stack.pop()
        dp, dq, i = node.dp_bits, node.dq_bits, node.bit_pos

        if i == bit_length:
            if is_valid(dp, dq, i, N):
                return dp, dq

        elif i < bit_length:
            dp = set_bit(dp, i, known_bits_dp[i])
            dq = set_bit(dq, i, known_bits_dq[i])

            valid_children = []

            def add_child_and_prune(dp_bits, dq_bits):
                if is_valid(dp_bits, dq_bits, i, N):
                    child_node = TreeNode(dp_bits, dq_bits, i + 1)
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
                    dq_bits_new = set_bit(dq, i, bit_dq)
                    dp_bits_new = dp
                    add_child_and_prune(dp_bits_new, dq_bits_new)

            else:
                add_child_and_prune(dp, dq)

            node.children = valid_children

    return None

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

def branch_and_prune(N, e, known_bits_dp, known_bits_dq):
    for kp in range(1, e):  # Assuming kp ranges from 1 to e-1
        result = build_tree_and_prune_dfs(N, e, kp, known_bits_dp, known_bits_dq)
        if result is not None:
            if verify_dp_dq(bits_to_int(result[0]), bits_to_int(result[1]), 29, 31, e):
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
