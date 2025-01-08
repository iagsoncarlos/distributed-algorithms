import time
import threading
from loguru import logger
from typing import Optional


class Zookeeper:
    """
    Simulates a basic Zookeeper service with node management and distributed lock functionality.

    Attributes:
        nodes (dict): A dictionary storing the nodes with their paths as keys and values as values.
        locks (dict): A dictionary storing the locked nodes with paths as keys and lock statuses as values.
        lock (threading.Lock): A threading lock used to ensure thread-safe operations on nodes and locks.
    """
    
    def __init__(self):
        """
        Initializes the Zookeeper simulation with an empty nodes dictionary,
        an empty locks dictionary, and a threading lock for synchronization.
        """
        self.nodes: dict[str, str] = {}  # Stores nodes (keys and values) in the simulated Zookeeper.
        self.locks: dict[str, str] = {}  # Tracks locked nodes with the client using the lock.
        self.lock = threading.Lock()  # Ensures exclusive access to data structures.
    
    def create_node(self, path: str, value: str) -> bool:
        """
        Creates a new node at the specified path with a given value.

        Args:
            path (str): The path where the node should be created.
            value (str): The value to assign to the node.

        Returns:
            bool: True if the node was created, False if the node already exists.
        """
        with self.lock:
            if path not in self.nodes:
                self.nodes[path] = value
                logger.info(f"Node created at {path} with value: {value}")
                return True
            else:
                logger.warning(f"Node at {path} already exists.")
                return False
    
    def get_node(self, path: str) -> Optional[str]:
        """
        Retrieves the value of the node at the specified path.

        Args:
            path (str): The path of the node to retrieve.

        Returns:
            Optional[str]: The value of the node if it exists, or None if the node does not exist.
        """
        with self.lock:
            return self.nodes.get(path)
    
    def set_node(self, path: str, value: str) -> bool:
        """
        Updates the value of an existing node at the specified path.

        Args:
            path (str): The path of the node to update.
            value (str): The new value to assign to the node.

        Returns:
            bool: True if the node was updated, False if the node does not exist.
        """
        with self.lock:
            if path in self.nodes:
                self.nodes[path] = value
                logger.info(f"Node at {path} updated with value: {value}")
                return True
            else:
                logger.warning(f"Node at {path} does not exist.")
                return False
    
    def lock_node(self, path: str, client_id: str) -> bool:
        """
        Acquires a lock for the node at the specified path by a client.

        Args:
            path (str): The path of the node to lock.
            client_id (str): The identifier of the client requesting the lock.

        Returns:
            bool: True if the lock was acquired, False if the node is already locked by another client.
        """
        with self.lock:
            if path not in self.locks:
                self.locks[path] = client_id
                logger.info(f"Lock acquired at {path} by client {client_id}.")
                return True
            else:
                current_client = self.locks[path]
                logger.warning(f"Node at {path} is already locked by client {current_client}.")
                return False
    
    def unlock_node(self, path: str, client_id: str) -> bool:
        """
        Releases the lock for the node at the specified path by a client.

        Args:
            path (str): The path of the node to unlock.
            client_id (str): The identifier of the client releasing the lock.

        Returns:
            bool: True if the lock was released, False if the node was not locked or the client is not the one holding the lock.
        """
        with self.lock:
            if path in self.locks and self.locks[path] == client_id:
                del self.locks[path]
                logger.info(f"Lock released at {path} by client {client_id}.")
                return True
            else:
                logger.warning(f"Client {client_id} failed to release lock at {path} (lock not held or held by another client).")
                return False


class DistributedLock:
    """
    Represents a distributed lock that can be acquired and released using Zookeeper.

    Attributes:
        zookeeper (Zookeeper): The Zookeeper instance used to manage locks.
        lock_path (str): The path of the node to lock and unlock.
        client_id (str): The unique identifier for the client.
    """

    def __init__(self, zookeeper: Zookeeper, lock_path: str, client_id: str):
        """
        Initializes the DistributedLock with the Zookeeper instance, lock path, and client ID.

        Args:
            zookeeper (Zookeeper): The Zookeeper instance used to manage locks.
            lock_path (str): The path of the node to lock and unlock.
            client_id (str): The unique identifier for the client.
        """
        self.zookeeper = zookeeper
        self.lock_path = lock_path
        self.client_id = client_id
    
    def acquire_lock(self) -> None:
        """
        Attempts to acquire the lock at the specified lock path by the client.

        This method will keep trying to acquire the lock until it succeeds. It simulates
        the behavior of a worker attempting to acquire a distributed lock and may retry
        with random delays if the lock is unavailable.
        """
        while not self.zookeeper.lock_node(self.lock_path, self.client_id):
            logger.debug(f"Client {self.client_id} waiting to acquire lock at {self.lock_path}...")
            time.sleep(2)  # Random delay before retrying.
    
    def release_lock(self) -> None:
        """
        Releases the lock at the specified lock path by the client.

        If the lock is successfully released, an info message is logged. If the lock was
        not previously acquired, an error message is logged.
        """
        if self.zookeeper.unlock_node(self.lock_path, self.client_id):
            logger.info(f"Client {self.client_id} released lock at {self.lock_path} successfully.")
        else:
            logger.error(f"Client {self.client_id} failed to release lock at {self.lock_path}.")


class Worker:
    """
    Simulates a worker attempting to acquire a distributed lock, perform work, and then release the lock.
    """

    def __init__(self, lock: DistributedLock) -> None:
        self.lock = lock

    def perform_task(self) -> None:
        """
        Simulate a worker's task: acquire lock, perform work, and release lock.
        """
        logger.info(f"Client {self.lock.client_id} attempting to acquire lock...")
        self.lock.acquire_lock()
        logger.info(f"Client {self.lock.client_id} acquired lock, performing work...")
        time.sleep(2)  # Simulating work
        logger.info(f"Client {self.lock.client_id} finished work, releasing lock.")
        self.lock.release_lock()
        logger.success(f"Client {self.lock.client_id} successfully finished the task and released the lock.")


if __name__ == "__main__":
    logger.info("Starting distributed lock simulator using zookeeper test.")
    
    zookeeper = Zookeeper()
    zookeeper.create_node("/distributed_lock", "initial_value")  # Create the lock node
    
    # Simulate multiple clients (with different client IDs) trying to acquire the lock
    threads: list[threading.Thread] = []
    for i in range(3):  # Simulate 3 clients attempting to acquire the lock
        lock = DistributedLock(zookeeper, "/distributed_lock", f"Client-{i+1}")
        worker_instance = Worker(lock)  # Instantiate worker with the lock
        t = threading.Thread(target=worker_instance.perform_task)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
