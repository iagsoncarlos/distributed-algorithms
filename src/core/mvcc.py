from loguru import logger
from typing import Any, Optional, Dict


class MVCC:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.transactions: Dict[int, Dict[str, Any]] = {}
        logger.info("Initialized MVCC system.")

    def begin_transaction(self, transaction_id: int) -> None:
        """
        Starts a new transaction.
        """
        if transaction_id in self.transactions:
            logger.error(f"Transaction {transaction_id} already exists.")
            raise ValueError(f"Transaction {transaction_id} already exists.")
        self.transactions[transaction_id] = {}
        logger.info(f"Transaction {transaction_id} started.")

    def write(self, transaction_id: int, key: str, value: Any) -> None:
        """
        Writes a value to a transaction's version of the data.
        """
        if transaction_id not in self.transactions:
            logger.error(f"Write failed: Transaction {transaction_id} does not exist.")
            raise ValueError(f"Transaction {transaction_id} does not exist.")
        self.transactions[transaction_id][key] = value
        logger.info(f"Transaction {transaction_id} wrote {key} = {value}.")

    def read(self, transaction_id: int, key: str, fallback_to_main: bool = True) -> Optional[Any]:
        """
        Reads a value from a transaction's version or the main data store.
        """
        if transaction_id not in self.transactions:
            if fallback_to_main:
                logger.warning(f"Transaction {transaction_id} not found. Reading from main data store.")
                return self.data.get(key)
            else:
                logger.error(f"Read failed: Transaction {transaction_id} does not exist.")
                return None

        value = self.transactions[transaction_id].get(key, self.data.get(key))
        logger.info(f"Transaction {transaction_id} read {key} = {value}.")
        return value

    def commit(self, transaction_id: int) -> None:
        """
        Commits a transaction's changes to the main data store.
        """
        if transaction_id not in self.transactions:
            logger.error(f"Commit failed: Transaction {transaction_id} does not exist.")
            raise ValueError(f"Transaction {transaction_id} does not exist.")
        
        for key, value in self.transactions[transaction_id].items():
            self.data[key] = value
            logger.info(f"Committed {key} = {value} to main data store.")
        
        del self.transactions[transaction_id]
        logger.success(f"Transaction {transaction_id} committed and cleared.")

    def rollback(self, transaction_id: int) -> None:
        """
        Rolls back a transaction, discarding its changes.
        """
        if transaction_id not in self.transactions:
            logger.error(f"Rollback failed: Transaction {transaction_id} does not exist.")
            raise ValueError(f"Transaction {transaction_id} does not exist.")
        
        del self.transactions[transaction_id]
        logger.warning(f"Transaction {transaction_id} rolled back and cleared.")

    def show_data(self) -> None:
        """
        Logs the current state of the main data store.
        """
        logger.info(f"Current main data store: {self.data}")


# Example Usage
if __name__ == "__main__":
    logger.info("Starting MVCC test.")

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
