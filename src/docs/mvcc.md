# Multi-Version Concurrency Control (MVCC) Documentation

This document describes the implementation of the Multi-Version Concurrency Control (MVCC) system, a technique for managing concurrent transactions in a database while maintaining data consistency. MVCC allows transactions to access data without blocking other transactions and supports rollback and commit operations to ensure atomicity.

---

## Overview

MVCC is used to handle concurrent data access by providing a snapshot of the data for each transaction. It allows multiple transactions to occur simultaneously without interfering with each other. The system maintains an isolated version of the data for each active transaction, and changes are only committed to the main data store once the transaction is committed. If a transaction is rolled back, any changes made during that transaction are discarded.

### Key Concepts
- **Transaction**: An operation or a series of operations performed as a single unit of work.
- **Versioning**: Each transaction maintains its own version of data until it commits or rolls back.
- **Commit**: Finalizes a transaction, making its changes permanent in the main data store.
- **Rollback**: Reverts any changes made by a transaction without affecting the main data store.
- **Snapshot Isolation**: Transactions are isolated from each other by providing a snapshot of the data at the start of the transaction.

---

## Class Definitions

### **MVCC Class**

The `MVCC` class implements the core functionality of the Multi-Version Concurrency Control system.

#### Attributes:
- `data` (`Dict[str, Any]`): The main data store that holds the current state of all data after commits.
- `transactions` (`Dict[int, Dict[str, Any]]`): A dictionary that stores the changes for each active transaction. Each transaction is identified by a unique `transaction_id`.

#### Methods:

1. **`__init__(self)`**:
   - Initializes the MVCC system, setting up the main data store (`data`) and transactions store (`transactions`).
   - Logs the initialization.
   - Example log: `Initialized MVCC system.`

2. **`begin_transaction(self, transaction_id: int) -> None`**:
   - Starts a new transaction.
   - Throws an error if the transaction ID already exists.
   - Logs the start of the transaction.
   - Example log: `Transaction 1 started.`

3. **`write(self, transaction_id: int, key: str, value: Any) -> None`**:
   - Writes a value to the data store for a given transaction.
   - Throws an error if the transaction does not exist.
   - Logs the write operation.
   - Example log: `Transaction 1 wrote key1 = value1.`

4. **`read(self, transaction_id: int, key: str, fallback_to_main: bool = True) -> Optional[Any]`**:
   - Reads a value for a transaction from either the transaction's version of the data or the main data store.
   - Logs the read operation and returns the value.
   - If the transaction doesn't exist and `fallback_to_main` is `True`, reads from the main data store.
   - Example log: `Transaction 1 read key1 = value1.`

5. **`commit(self, transaction_id: int) -> None`**:
   - Commits the changes of a transaction to the main data store.
   - Deletes the transaction from the transactions store after the commit.
   - Logs the commit operation.
   - Example log: `Transaction 1 committed and cleared.`

6. **`rollback(self, transaction_id: int) -> None`**:
   - Rolls back a transaction, discarding its changes.
   - Deletes the transaction from the transactions store after the rollback.
   - Logs the rollback operation.
   - Example log: `Transaction 2 rolled back and cleared.`

7. **`show_data(self) -> None`**:
   - Logs the current state of the main data store.
   - Example log: `Current main data store: {'key1': 'value1'}`

---

## Usage Example

The following example demonstrates how to use the `MVCC` class to manage transactions, including committing and rolling back transactions.

### Code Example:
```python
from mvcc import MVCC

# Initialize the MVCC system
db = MVCC()

# Start a transaction, write data, and commit it
db.begin_transaction(1)
db.write(1, "key1", "value1")
logger.info(f"Read key1 in transaction 1: {db.read(1, 'key1')}")
db.commit(1)

# Show the committed state
db.show_data()

# Start another transaction and perform a rollback
db.begin_transaction(2)
db.write(2, "key2", "value2")
logger.info(f"Read key2 in transaction 2: {db.read(2, 'key2')}")
logger.error(f"Error saving information to the database")
db.rollback(2)

# Attempt to read key2 after rollback (should not exist)
logger.info(f"Read key2 after rollback: {db.read(2, 'key2', fallback_to_main=True)}")

# Show the final state of the main data store
db.show_data()
```

### Output Explanation:
1. **Transaction 1**: The value `key1 = value1` is written, read, and committed to the main data store.
2. **Transaction 2**: The value `key2 = value2` is written, read, but then rolled back, leaving the main data store unchanged.
3. **Final State**: After rollback, `key2` does not exist in the main data store.

---

## Log Structure

The system uses `loguru` for logging detailed information at each stage.

### Example Logs:
- **Info**: Logs general operations such as starting transactions, committing data, and reading values.
  - Example: `Transaction 1 started.`
- **Warning**: Logs warnings when reading from the main data store if a transaction is not found.
  - Example: `Transaction 2 not found. Reading from main data store.`
- **Error**: Logs errors such as trying to start an already existing transaction or attempting operations on a non-existent transaction.
  - Example: `Write failed: Transaction 3 does not exist.`
- **Success**: Logs successful commits.
  - Example: `Transaction 1 committed and cleared.`

---

## Advantages and Considerations

### Advantages:
- **Concurrency**: Multiple transactions can occur simultaneously, improving performance in highly concurrent environments.
- **Isolation**: Each transaction operates on its own version of the data, ensuring isolation from other transactions.
- **Consistency**: Transactions either commit their changes or roll them back, maintaining consistency in the system.

### Limitations:
- **Space Overhead**: Each transaction maintains its own version of the data, which may require more storage.
- **Snapshot Staleness**: Transactions are isolated, which may lead to inconsistencies in data views if transactions read data from different versions.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install loguru
   ```
2. Run the script:
   ```bash
   python src/core/mvcc.py
   ```

---

## Test Cases

Below are the test cases that validate the functionality of the MVCC system:

### 1. **Test Case 1: Begin a Transaction and Commit**
   - **Steps**:
     1. Start a new transaction.
     2. Write data to the transaction.
     3. Commit the transaction.
   - **Expected Outcome**: 
     - The data should be committed to the main data store and visible in subsequent reads.

### 2. **Test Case 2: Begin a Transaction and Rollback**
   - **Steps**:
     1. Start a new transaction.
     2. Write data to the transaction.
     3. Rollback the transaction.
   - **Expected Outcome**: 
     - The data should not be committed to the main data store and should be discarded.

### 3. **Test Case 3: Read from a Transaction that Does Not Exist**
   - **Steps**:
     1. Attempt to read from a transaction that has not been started.
   - **Expected Outcome**: 
     - The system should log an error and, if configured, return data from the main data store.

### 4. **Test Case 4: Handle Writing to a Non-Existent Transaction**
   - **Steps**:
     1. Attempt to write data to a non-existent transaction.
   - **Expected Outcome**: 
     - The system should throw an error indicating that the transaction does not exist.

### 5. **Test Case 5: Handling Invalid Commit and Rollback**
   - **Steps**:
     1. Attempt to commit or rollback a transaction that does not exist.
   - **Expected Outcome**: 
     - The system should raise an error indicating the transaction does not exist.

---

## Notes

- **Concurrency**: This implementation of MVCC does not handle concurrent transaction management. In a production environment, further enhancements may be required for handling concurrency control, such as using locks or timestamps.
- **Performance**: While MVCC allows for concurrent reads, excessive versioning could lead to increased memory usage, especially with a large number of transactions.
- **Error Handling**: The system raises `ValueError` when attempting to perform an operation on a non-existent transaction, ensuring that invalid operations are properly handled.
  
