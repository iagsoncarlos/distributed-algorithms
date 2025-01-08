# Chandy-Lamport Algorithm Implementation

## Overview

This documentation details the implementation of the **Chandy-Lamport Algorithm** in Python. This algorithm is designed for distributed systems to capture global states in a consistent manner. The implementation includes core functionalities for message passing, snapshot capturing, and snapshot retrieval.

## Features

- **Simulated Message Passing**: Send messages between processes in a distributed system.
- **Snapshot Capture**: Record the state of processes and their received messages.
- **Snapshot Retrieval**: Access previously captured snapshots.

---

## Class: `ChandyLamport`

### Initialization

#### `__init__()`
Initializes the internal state of the system.
- **Attributes**:
  - `channels`: A dictionary to store messages sent to processes.
  - `snapshots`: A dictionary to store snapshots of processes.

**Example Usage**:
```python
system = ChandyLamport()
```

---

### Methods

#### `send_message(sender: str, receiver: str, message: str) -> None`

Simulates sending a message from one process to another.

- **Args**:
  - `sender` (str): ID of the process sending the message.
  - `receiver` (str): ID of the process receiving the message.
  - `message` (str): Content of the message.

- **Logs**:
  - Debug: Details of the message being sent.
  - Info: Confirmation of message delivery and channel state update.

**Example Usage**:
```python
system.send_message("A", "B", "Hello, B!")
```

---

#### `capture_snapshot(process_id: str) -> None`

Captures the state of a process, including messages it has received.

- **Args**:
  - `process_id` (str): ID of the process whose state is to be captured.

- **Logs**:
  - Debug: Snapshot capture details and updated snapshot state.
  - Info: Confirmation of snapshot capture.

- **Snapshot Structure**:
  ```python
  {
      "received_messages": list[str],  # Messages received by the process.
      "state": str,  # Placeholder for process state.
  }
  ```

**Example Usage**:
```python
system.capture_snapshot("A")
```

---

#### `get_snapshot(process_id: str) -> Optional[dict[str, list[str] | str]]`

Retrieves the snapshot of a specified process.

- **Args**:
  - `process_id` (str): ID of the process whose snapshot is required.

- **Returns**:
  - `dict[str, list[str] | str]`: Snapshot of the process, or `None` if no snapshot is available.

- **Logs**:
  - Debug: Retrieval request and snapshot details.
  - Info: Successful retrieval.
  - Warning: If no snapshot is found.

**Example Usage**:
```python
snapshot = system.get_snapshot("A")
if snapshot:
    print(snapshot)
else:
    print("No snapshot available.")
```

---

## Example Program

```python
from loguru import logger

if __name__ == "__main__":
    logger.info("Starting Chandy-Lamport example system.")

    # Initialize the system
    system = ChandyLamport()

    # Simulate message passing
    logger.info("Sending message from process A to process B.")
    system.send_message("A", "B", "Message 1")

    # Capture snapshots for processes
    logger.info("Capturing snapshot for process A.")
    system.capture_snapshot("A")

    logger.info("Capturing snapshot for process B.")
    system.capture_snapshot("B")

    # Retrieve and print all snapshots
    logger.info("Retrieving and printing all snapshots.")
    for process_id in ["A", "B"]:
        snapshot = system.get_snapshot(process_id)
        logger.debug(f"Process {process_id} snapshot: {snapshot}")
```

---

## Logging

The implementation uses the `loguru` library for logging. Log messages include detailed debug information, warnings, and general information logs.

- **Info Logs**:
  - Initialization of the system.
  - Confirmation of message sending.
  - Confirmation of snapshot capture.
  - Retrieval status of snapshots.

- **Debug Logs**:
  - Detailed internal state changes for channels and snapshots.

- **Warning Logs**:
  - Missing snapshots during retrieval.

---

## Installation

1. Install Python 3.9+.
2. Install `loguru`:
   ```bash
   pip install loguru
   ```
3. Run the script:
   ```bash
   python src/core/chandy_lamport.py
---

## Notes

- The `state` field in snapshots is currently a placeholder. You can replace it with actual state capture logic.
- The implementation assumes a centralized logging system using `loguru`.

---

## Limitations

- The implementation does not handle concurrent message sending or snapshot capturing.
- The `state` field requires process-specific implementation for meaningful state capture.

---

## References

- Chandy, K. M., & Lamport, L. (1985). Distributed snapshots: Determining global states of distributed systems. *ACM Transactions on Computer Systems (TOCS)*.
