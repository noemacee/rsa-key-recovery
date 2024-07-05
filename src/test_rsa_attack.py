import time
import tracemalloc
from helpers import bits_to_int
from crt_pruning import branch_and_prune_crt
from rsa import generate_prime

def generate_test_data(bit_length, e):
    """
    Generate test data for the performance test.
    
    :param bit_length: Bit length of the prime factors p and q.
    :param e: Public exponent.
    :return: Tuple of (N, known_bits_dp, known_bits_dq)
    """
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    N = p * q
    dp = pow(p, -1, e)
    dq = pow(q, -1, e)
    
    # Convert to bit representation
    known_bits_dp = [int(bit) for bit in bin(dp)[2:]]
    known_bits_dq = [int(bit) for bit in bin(dq)[2:]]
    
    # Introduce unknowns (set some bits to -1)
    for i in range(0, len(known_bits_dp), 3):
        known_bits_dp[i] = -1
    for i in range(0, len(known_bits_dq), 4):
        known_bits_dq[i] = -1
    
    return N, known_bits_dp, known_bits_dq

def performance_test(bit_length, e):
    """
    Perform the performance test.
    
    :param bit_length: Bit length of the prime factors p and q.
    :param e: Public exponent.
    """
    N, known_bits_dp, known_bits_dq = generate_test_data(bit_length, e)
    
    # Start measuring time and memory
    start_time = time.time()
    tracemalloc.start()
    
    result = branch_and_prune_crt(N, e, known_bits_dp, known_bits_dq)
    
    # Stop measuring memory
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    
    if result is None:
        print("No solution found")
        return
    
    p, q, dp, dq, root_node, kp, kq = result
    p = bits_to_int(p)
    q = bits_to_int(q)
    dp = bits_to_int(dp)
    dq = bits_to_int(dq)
    
    print(f"Test with bit length {bit_length}:")
    print(f"Execution time: {end_time - start_time} seconds")
    print(f"Current memory usage: {current / 10**6} MB")
    print(f"Peak memory usage: {peak / 10**6} MB")
    print(f"Recovered p: {p}")
    print(f"Recovered q: {q}")
    print(f"Recovered dp: {dp}")
    print(f"Recovered dq: {dq}")
    print(f"Recovered kp: {kp}")
    print(f"Recovered kq: {kq}")
    print()

# Perform tests with different bit lengths
for bit_length in [8, 16, 32]:
    performance_test(bit_length, 17)
