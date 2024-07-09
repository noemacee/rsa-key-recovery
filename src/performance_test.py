from helpers import *
from branch_prune import branch_and_prune
from crt_pruning import branch_and_prune_crt
import time
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

def run_branch_prune(revealrate, bitsize):
    """
    Run the first algorithm with a given reveal rate and bit size and measure the time taken.

    :param revealrate: The rate at which bits are revealed (0 to 1).
    :param bitsize: The desired bitsize for p and q.
    :return: Time taken to run the algorithm.
    """
    start_time = time.time()
    
    # Generate example values
    N, p, q, p_bits, q_bits, p_erased, q_erased = example_generator(revealrate, bitsize)

    # Run the branch and prune algorithm
    result = branch_and_prune(N, p_erased, q_erased)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, result

def run_crt_pruning(revealrate, bitsize, e=17):
    """
    Run the second algorithm with CRT pruning, given a reveal rate, bit size, and public exponent e, and measure the time taken.

    :param revealrate: The rate at which bits are revealed (0 to 1).
    :param bitsize: The desired bitsize for p and q.
    :param e: The public exponent (default is 17).
    :return: Time taken to run the algorithm.
    """
    start_time = time.time()
    
    # Generate example values for CRT pruning
    N, dp_bits, dq_bits, dp, dq, dp_erased, dq_erased, p, q = example_generator_crt_pruning(revealrate, bitsize, e)

    # Run the branch and prune algorithm
    result = branch_and_prune_crt(N, e, dp_erased, dq_erased)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, result

import math

def fermat_factorization(N):
    """
    Factorize N using Fermat's factorization method.

    :param N: The number to factorize.
    :return: A tuple (p, q) if factors are found, else (None, None).
    """
    if N % 2 == 0:
        return N // 2, 2  # Handle even N case

    a = math.ceil(math.sqrt(N))
    b2 = a * a - N
    b = math.isqrt(b2)

    while b * b != b2:
        a += 1
        b2 = a * a - N
        b = math.isqrt(b2)

    p = a - b
    q = a + b

    return p, q

def run_fermat_factorization(revealrate, bitsize):
    """
    Run the Fermat factorization algorithm with a given reveal rate and bit size and measure the time taken.

    :param revealrate: The rate at which bits are revealed (0 to 1).
    :param bitsize: The desired bitsize for p and q.
    :return: Time taken to run the algorithm.
    """
    N, p, q, p_bits, q_bits, p_erased, q_erased = example_generator(revealrate, bitsize)

    start_time = time.time()
    result = fermat_factorization(N)
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time, result

def test_algorithm1(bitsize=10):
    revealrate_values = [i * 0.05 for i in range(1, 21)]  # From 0.1 to 1.0
    algorithm1_times = []

    for revealrate in revealrate_values:
        print("\nRunning Algorithm 1 with reveal rate", revealrate)
        time_taken_alg1, result_alg1 = run_branch_prune(revealrate, bitsize)
        algorithm1_times.append(time_taken_alg1)

        # Print results for current reveal rate
        print(f"\nReveal Rate: {revealrate}")
        print(f"Algorithm 1 Time: {time_taken_alg1:.4f} seconds, Result: {'Found' if result_alg1 else 'Not Found'}")

    # Plot results for Algorithm 1
    plt.figure(figsize=(10, 6))
    plt.plot(revealrate_values, algorithm1_times, marker='o', label='Algorithm 1')
    plt.title('Performance of Algorithm 1')
    plt.xlabel('Reveal Rate')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()

def test_algorithm2(bitsize=10, e=17):
    revealrate_values = [i * 0.1 for i in range(5, 11)]  # From 0.1 to 1.0
    algorithm2_times = []

    for revealrate in revealrate_values:
        print("\nRunning Algorithm 2 with reveal rate", revealrate)
        time_taken_alg2, result_alg2 = run_crt_pruning(revealrate, bitsize, e)
        algorithm2_times.append(time_taken_alg2)

        # Print results for current reveal rate
        print(f"\nReveal Rate: {revealrate}")
        print(f"Algorithm 2 Time: {time_taken_alg2:.4f} seconds, Result: {'Found' if result_alg2 else 'Not Found'}")

    # Plot results for Algorithm 2
    plt.figure(figsize=(10, 6))
    plt.plot(revealrate_values, algorithm2_times, marker='o', label='Algorithm 2')
    plt.title('Performance of Algorithm 2')
    plt.xlabel('Reveal Rate')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_algorithms(bitsize=10, e=17):
    revealrate_values = [i * 0.1 for i in range(5, 11)]  # From 0.5 to 1.0
    algorithm1_times = []
    algorithm2_times = []
    fermat_times = []

    for revealrate in revealrate_values:
        print("\nRunning algorithms with reveal rate", revealrate)

        # Run Algorithm 1
        time_taken_alg1, result_alg1 = run_branch_prune(revealrate, bitsize)
        algorithm1_times.append(time_taken_alg1)
        print(f"Algorithm 1 Time: {time_taken_alg1:.4f} seconds, Result: {'Found' if result_alg1 else 'Not Found'}")

        # Run Algorithm 2
        time_taken_alg2, result_alg2 = run_crt_pruning(revealrate, bitsize, e)
        algorithm2_times.append(time_taken_alg2)
        print(f"Algorithm 2 Time: {time_taken_alg2:.4f} seconds, Result: {'Found' if result_alg2 else 'Not Found'}")

        # Run Fermat Factorization
        time_taken_fermat, result_fermat = run_fermat_factorization(revealrate, bitsize)
        fermat_times.append(time_taken_fermat)
        print(f"Fermat Factorization Time: {time_taken_fermat:.4f} seconds, Result: {'Found' if result_fermat else 'Not Found'}")

    # Plot results for all algorithms
    plt.figure(figsize=(10, 6))
    plt.plot(revealrate_values, algorithm1_times, marker='o', label='Algorithm 1')
    plt.plot(revealrate_values, algorithm2_times, marker='s', label='Algorithm 2')
    plt.plot(revealrate_values, fermat_times, marker='^', label='Fermat Factorization')
    plt.title('Performance Comparison of Algorithms')
    plt.xlabel('Reveal Rate')
    plt.ylabel('Time Taken (seconds)')
    plt.legend()
    plt.grid(True)
    plt.show()
