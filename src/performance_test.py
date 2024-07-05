from helpers import *
from branch_prune import branch_and_prune
from crt_pruning import branch_and_prune_crt
import time
#import matplotlib.pyplot as plt

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
    result = branch_and_prune(N, dp_erased, dq_erased)

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return elapsed_time, result

def performance_test(revealrate_values, bitsize=10, e=17):
    """
    Perform performance tests for both algorithms over different reveal rates and plot the results.

    :param revealrate_values: List of reveal rate values to test.
    :param bitsize: The desired bitsize for p and q.
    :param e: The public exponent (default is 17).
    """
    algorithm1_times = []
    algorithm2_times = []

    for revealrate in revealrate_values:
        # Test algorithm 1
        time_taken_alg1, result_alg1 = run_branch_prune(revealrate, bitsize)
        algorithm1_times.append(time_taken_alg1)

        # Test algorithm 2
        time_taken_alg2, result_alg2 = run_crt_pruning(revealrate, bitsize, e)
        algorithm2_times.append(time_taken_alg2)

        # Print results for current reveal rate
        print(f"\nReveal Rate: {revealrate}")
        print(f"Algorithm 1 Time: {time_taken_alg1:.4f} seconds, Result: {'Found' if result_alg1 else 'Not Found'}")
        print(f"Algorithm 2 Time: {time_taken_alg2:.4f} seconds, Result: {'Found' if result_alg2 else 'Not Found'}")

    # Plot results
    # plt.figure(figsize=(10, 6))
    # plt.plot(revealrate_values, algorithm1_times, marker='o', label='Algorithm 1')
    # plt.plot(revealrate_values, algorithm2_times, marker='o', label='Algorithm 2')
    # plt.title('Performance Comparison of Algorithms')
    # plt.xlabel('Reveal Rate')
    # plt.ylabel('Time Taken (seconds)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

# Example usage with a range of reveal rate values
revealrate_values = [i * 0.1 for i in range(1, 11)]  # From 0.1 to 1.0

performance_test(revealrate_values)