# RSA CRT Pruning Algorithm

## Overview

This project demonstrates techniques used to recover RSA parameters when given non-consecutive bits known with redundancy on its secret values. The main focus is on two algorithms:
1. Branch and Prune Algorithm
2. Chinese Remainder Theorem Pruning Algorithm

## Features

- **Branch and Prune Algorithm**: Recovers RSA parameters \(p\) and \(q\) given partial bits of \(p\) and \(q\).
- **Chinese Remainder Theorem Pruning Algorithm**: Recovers RSA parameters \(p\), \(q\), \(dp\), and \(dq\) given partial bits of \(dp\) and \(dq\).
- **Performance Testing**: Measures the efficiency of the algorithms.
- **Tree Structure Printing**: Visualizes the tree structure used in the pruning process.

## Installation

1. **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Dependencies**
    ```bash
    pip install sympy
    ```

## Usage

### Command-Line Arguments

- `--test`: Run performance tests.
- `--revealrate`: Bit reveal rate for testing (default: 0.5).
- `--bitsize`: Bit size for RSA components (default: 10).
- `--e`: Public exponent for RSA (default: 17).
- `--print_tree`: Print the tree structure of the solutions.

### Running the Script

1. **Run Performance Tests**
    ```bash
    python main.py --test
    ```

2. **Run Branch and Prune Algorithm**
    ```bash
    python main.py
    ```

### Example Output

The script will output the recovered RSA parameters and optionally print the tree structure used in the pruning process.

## Performance Testing

The performance test runs the algorithms for different bit sizes and reveal rates and measures their efficiency.

```bash
python main.py --test --bitsize 32 --revealrate 0.5
```



