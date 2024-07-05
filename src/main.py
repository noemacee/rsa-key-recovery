import argparse
from performance_test import performance_test
from crt_pruning import branch_and_prune_crt
from branch_prune import branch_and_prune
from helpers import print_tree, example_generator, example_generator_crt_pruning, bits_to_int

def main():
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='RSA CRT Pruning Algorithm')
    parser.add_argument('--test', action='store_true', help='Run performance tests')
    parser.add_argument('--revealrate', type=float, default=0.5, help='Bit reveal rate for testing')
    parser.add_argument('--bitsize', type=int, default=10, help='Bit size for RSA components')
    parser.add_argument('--e', type=int, default=17, help='Public exponent for RSA')
    parser.add_argument('--print_tree', action='store_true', help='Print the tree structure of the solutions')
    args = parser.parse_args()

    if args.test:
        performance_test(args.bitsize, args.e)
    else:
        # Algorithm 1: branch_prune with textbook example
        print("Algorithm 1: Branch and Prune with Textbook Example")
        print("Textbook example with N = 899, p = 31, q = 29\n")
        N = 899
        known_bits_p = [-1, 1, 1, -1, 1]
        known_bits_q = [-1, 1, -1, 0, -1]

        # Find the factors p and q
        result = branch_and_prune(N, known_bits_p, known_bits_q)

        if result is None:
            print("No solution found")
        else:
            p, q = result
            print(f"Recovered p: {p[::-1]}")
            print(f"Recovered q: {q[::-1]}")
            print(f"p as int: {bits_to_int(p)}")
            print(f"q as int: {bits_to_int(q)}")

        # Example usage of example_generator
        print("\nExample using example_generator with provided revealrate and bitsize\n")
        revealrate = args.revealrate
        bitsize = args.bitsize

        N, p, q, p_actual, q_actual, p_erased, q_erased = example_generator(revealrate, bitsize)

        print("Generated Values:")
        print(f"N: {N}")
        
        print(f"p as int: {p}")
        print(f"q as int: {q}")

         # Print the bit representations
        print("Bit Representations:")
        print(f"p_bits: {p_actual}")
        print(f"q_bits: {q_actual}")

        # Print the erased bit representations
        print("Erased Bit Representations:")
        print(f"p_erased: {p_erased}")
        print(f"q_erased: {q_erased}")

        # Find the factors p and q
        result = branch_and_prune(N, p_erased, q_erased)

        if result is None:
            print("No solution found")
        else:
            p, q = result
            print("Solution Found:")
            print(f"Recovered p: {p[::-1]}")
            print(f"Recovered q: {q[::-1]}")
            print(f"p as int: {bits_to_int(p)}")
            print(f"q as int: {bits_to_int(q)}")

        # Algorithm 2: crt_pruning with textbook example
        print("\nAlgorithm 2: CRT Pruning with Textbook Example")
        print("Textbook example with N = 899, dp = 23, dq = 5\n")
        N = 899
        e = 17
        known_bits_dp = [-1, 0, -1, -1, 1]
        known_bits_dq = [-1, -1, -1, 0, -1]

        result = branch_and_prune_crt(N, e, known_bits_dp, known_bits_dq)

        if result is None:
            print("No solution found")
        else:
            p, q, dp, dq, root_node, kp, kq = result
            p = bits_to_int(p)
            q = bits_to_int(q)
            dp = bits_to_int(dp)
            dq = bits_to_int(dq)

            if args.print_tree:
                # Print the tree structure
                print("Tree Structure:")
                print_tree(root_node)
                print()

            print("Solution found:")
            print(f"Recovered p: {p}")
            print(f"Recovered q: {q}")
            print(f"Recovered dp: {dp}")
            print(f"Recovered dq: {dq}")
            print(f"Recovered kp: {kp}")
            print(f"Recovered kq: {kq}")

        # Example usage of example_generator_crt
        print("\nExample using example_generator_crt with provided revealrate and bitsize\n")
        e = args.e
        revealrate = args.revealrate
        bitsize = args.bitsize

        # Generate example values for CRT pruning
        N, dp_bits, dq_bits, dp, dq, dp_erased, dq_erased, p, q = example_generator_crt_pruning(revealrate, bitsize, e)

        # Print the generated values
        print("Generated Values:")
        print(f"N: {N}")
        print(f"p (as int): {p}")
        print(f"q (as int): {q}")
        print(f"dp (as int): {dp}")
        print(f"dq (as int): {dq}")
        print()

        # Print the bit representations
        print("Bit Representations:")
        print(f"dp_bits: {dp_bits}")
        print(f"dq_bits: {dq_bits}")
        print()

        # Print the erased bit representations
        print("Erased Bit Representations:")
        print(f"dp_erased: {dp_erased}")
        print(f"dq_erased: {dq_erased}")
        print()

        # Attempt to find the factors p and q using the branch and prune algorithm
        print("Finding factors p and q using branch and prune algorithm...")
        result = branch_and_prune_crt(N, e, dp_erased, dq_erased)

        if result is None:
            print("No solution found.")
        else:
            p, q, dp, dq, root_node, kp, kq = result
            p = bits_to_int(p)
            q = bits_to_int(q)
            dp = bits_to_int(dp)
            dq = bits_to_int(dq)

            if args.print_tree:
                # Print the tree structure
                print("Tree Structure:")
                print_tree(root_node)
                print()
            

            # Print the recovered values
            print("Solution Found:")
            print(f"Recovered p: {p}")
            print(f"Recovered q: {q}")
            print(f"Recovered dp: {dp}")
            print(f"Recovered dq: {dq}")
            print(f"Recovered kp: {kp}")
            print(f"Recovered kq: {kq}")

if __name__ == '__main__':
    main()
