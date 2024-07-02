from sympy import mod_inverse

def find_kq_from_kp(kp, N, e):
    """
    Find the unique value of kq given kp, N, and e.
    
    Args:
    kp (int): The coefficient related to p.
    N (int): The known value N.
    e (int): The modulus.
    
    Returns:
    int: The unique value of kq.
    """
    lhs = kp - 1 - kp * N
    rhs = kp - 1
    
    lhs_inv = mod_inverse(lhs, e)
    if lhs_inv is None:
        raise ValueError("Modular inverse does not exist, ensure kp and e are coprime.")
    
    kq = (rhs * lhs_inv) % e
    
    return kq

def check_kq(kp, kq, N, e):
    """
    Check if the value of kq satisfies the given equation.
    
    Args:
    kp (int): The coefficient related to p.
    kq (int): The coefficient related to q.
    N (int): The known value N.
    e (int): The modulus.
    
    Returns:
    bool: True if the equation is satisfied, False otherwise.
    """
    left_hand_side = (kp - 1) * (kq - 1) % e
    right_hand_side = kp * kq * N % e
    
    return left_hand_side == right_hand_side

# Example usage:
kp = 6789  # Example value for kp
N = 54321  # Example value for N
e = 98765  # Example value for e

kq = find_kq_from_kp(kp, N, e)
print("The value of kq is:", kq)

# Check if kq is correct
is_correct = check_kq(kp, kq, N, e)
print("Is kq correct?", is_correct)
