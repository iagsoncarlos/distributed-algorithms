# Distributed Algorithms

Welcome to the Distributed Algorithms, a Python-based solution that enables the execution of various distributed algorithms for simulation and analysis. This project includes implementations of the Chandy-Lamport snapshot algorithm, MVCC (Multi-Version Concurrency Control), One-Phase Commit, Two-Phase Commit, and a Distributed Lock simulation.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Command-Line Arguments](#command-line-arguments)
- [Usage](#usage)
- [Algorithms Documentation](#algorithms-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Distributed Algorithms is a flexible tool designed for simulating and testing various distributed systems algorithms. By running different algorithms, you can observe their behavior and interactions in distributed environments. This project is a great starting point for understanding the workings of key algorithms used in distributed computing.

## Key Features

- **Algorithm Simulation:** Supports Chandy-Lamport, MVCC, One-Phase Commit, Two-Phase Commit, and Distributed Lock algorithms.
- **Snapshot Capture:** Run the Chandy-Lamport algorithm to capture distributed system snapshots.
- **Concurrency Control:** Simulate MVCC transactions with support for commit and rollback operations.
- **Commit Protocols:** Implement One-Phase Commit and Two-Phase Commit protocols with support for participant vote handling.
- **Distributed Lock:** Simulate distributed lock acquisition and usage with Zookeeper coordination.

## Dependencies

- **loguru**: For logging purposes.
- **argparse**: For argument parsing in the command-line interface.
- **threading**: For simulating concurrent workers in the distributed lock algorithm.

## Getting Started

To get started with running distributed algorithms, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/distributed-algorithms.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd distributed-algorithms
   ```

3. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install Project Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Development Environment

For a smooth development experience, it's recommended to use a Python virtual environment:

1. **Create a Development Environment:**
   ```bash
   python -m venv venv
   ```

2. **Install Dependencies:**
   Install the necessary dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

## Command-Line Arguments

### `algorithm`
Specifies which algorithm to run. Valid values are:

- `chandy_lamport`
- `mvcc`
- `one_phase_commit`
- `two_phase_commit`
- `distributed_lock`

### `--log`
Set the logging level. Valid values are:

- `debug`
- `info`
- `warning`
- `error`
- `critical`

**Default:** `info`

## Usage

To run a specific distributed algorithm, execute the following command:

1. **Run Chandy-Lamport Algorithm:**
   ```bash
   python main.py chandy_lamport --log info
   ```

2. **Run MVCC Algorithm:**
   ```bash
   python main.py mvcc --log info
   ```

3. **Run One-Phase Commit Algorithm:**
   ```bash
   python main.py one_phase_commit --log info
   ```

4. **Run Two-Phase Commit Algorithm:**
   ```bash
   python main.py two_phase_commit --log info
   ```

5. **Run Distributed Lock Simulation:**
   ```bash
   python main.py distributed_lock --log info
   ```

In each of these cases, the `--log` option allows you to control the logging level, which can be one of the following: `debug`, `info`, `warning`, `error`, `critical`.

## Algorithms Documentation

For detailed information on each distributed algorithm implemented in this project, please refer to the individual documentation sections below:

- **[Chandy-Lamport Snapshot Algorithm](src/docs/chandy-lamport.md)**
- **[MVCC (Multi-Version Concurrency Control)](src/docs/mvcc.md)**
- **[One-Phase Commit Protocol](src/docs/one-phase-commit.md)**
- **[Two-Phase Commit Protocol](src/docs/two-phase-commit.md)**
- **[Distributed Lock Simulation](src/docs/distributed-lock.md)**

Each link provides a comprehensive guide to understanding the algorithm's implementation, use cases, and technical details.

## Contributing

We welcome contributions to improve the Distributed Algorithms! If you’d like to contribute, please follow these steps:

1. **Fork the Repository:** Start by forking the repository to your own GitHub account.

2. **Create a New Branch:** Create a new branch for your feature or bug fix.

3. **Make Your Changes:** Implement your changes and improvements.

4. **Submit a Pull Request:** Submit a pull request, and our team will review your contribution.

Please ensure you follow our [Contributing Guidelines](CONTRIBUTING.md) and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software for personal or commercial purposes.