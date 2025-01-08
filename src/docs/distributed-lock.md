# Distributed Lock System using Zookeeper Simulation

## Overview

This code simulates a distributed lock system using a simplified Zookeeper service. It allows multiple clients to safely acquire and release locks on shared resources in a concurrent environment. The simulation includes a Zookeeper-like service, a distributed lock abstraction, and a worker class to demonstrate the lock's functionality.

## Features

- Simulates Zookeeper's node management and locking mechanism.
- Provides thread-safe operations for creating, updating, locking, and unlocking nodes.
- Implements a distributed lock system with retry mechanisms for contention resolution.
- Includes a worker class to simulate clients performing tasks with distributed locks.
- Logs events using the `loguru` library for detailed monitoring.

---

## Classes and Methods

### **Zookeeper**
Simulates a basic Zookeeper service with node management and distributed lock functionality.

#### Attributes:
- `nodes` (dict): Stores the nodes and their values.
- `locks` (dict): Tracks locks on nodes with client ownership.
- `lock` (threading.Lock): Ensures thread-safe operations.

#### Methods:
1. **`create_node(path: str, value: str) -> bool`**
   - Creates a node at a specified path with the given value.
   - Returns `True` if the node is created, `False` if it already exists.

2. **`get_node(path: str) -> Optional[str]`**
   - Retrieves the value of a node by its path.
   - Returns the value or `None` if the node does not exist.

3. **`set_node(path: str, value: str) -> bool`**
   - Updates the value of an existing node.
   - Returns `True` if updated, `False` if the node does not exist.

4. **`lock_node(path: str, client_id: str) -> bool`**
   - Attempts to acquire a lock on a node for a client.
   - Returns `True` if successful, `False` if the node is already locked.

5. **`unlock_node(path: str, client_id: str) -> bool`**
   - Releases the lock on a node held by a client.
   - Returns `True` if successful, `False` otherwise.

---

### **DistributedLock**
Represents a distributed lock acquired and released using Zookeeper.

#### Attributes:
- `zookeeper` (Zookeeper): The Zookeeper instance managing locks.
- `lock_path` (str): Path of the node to lock and unlock.
- `client_id` (str): Identifier of the client using the lock.

#### Methods:
1. **`acquire_lock()`**
   - Attempts to acquire a lock at the specified path.
   - Retries with a delay until the lock is acquired.

2. **`release_lock()`**
   - Releases the lock at the specified path if held by the client.

---

### **Worker**
Simulates a client performing a task using a distributed lock.

#### Attributes:
- `lock` (DistributedLock): The lock used by the worker.

#### Methods:
1. **`perform_task()`**
   - Acquires the lock, performs work, and releases the lock.

---

## Usage

### Example Execution
The main block initializes a Zookeeper instance, creates a node for the distributed lock, and spawns threads simulating multiple clients attempting to acquire the lock.

#### Key Steps:
1. **Create the Lock Node**:
   ```python
   zookeeper.create_node("/distributed_lock", "initial_value")
   ```
2. **Simulate Multiple Clients**:
   ```python
   threads = []
   for i in range(3):
       lock = DistributedLock(zookeeper, "/distributed_lock", f"Client-{i+1}")
       worker_instance = Worker(lock)
       t = threading.Thread(target=worker_instance.perform_task)
       threads.append(t)
       t.start()
   for t in threads:
       t.join()
   ```

---

## Logging

The `loguru` library is used for detailed logging:
- **Info Logs**: Successful operations (e.g., node creation, lock acquisition).
- **Warning Logs**: Conflicts or non-critical issues (e.g., node already exists, lock contention).
- **Error Logs**: Failed operations (e.g., unauthorized lock release).
- **Success Logs**: Task completion milestones.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install loguru
   ```
2. Run the script:
   ```bash
   python src/core/distributed_lock.py
   ```
3. Observe logs for lock contention and resolution among clients.

---

## Notes

- This simulation does not implement network communication and is designed for educational purposes.
- Thread safety is ensured using Python's `threading.Lock`.
- Delays between retries mimic real-world contention scenarios.
