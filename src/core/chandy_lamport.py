from loguru import logger
from typing import Optional


class ChandyLamport:
    def __init__(self):
        """
        Initializes the Chandy-Lamport algorithm state.
        """
        self.channels: dict[str, list[str]] = {}
        self.snapshots: dict[str, dict[str, list[str] | str]] = {}
        logger.info("Chandy-Lamport system initialized.")

    def send_message(self, sender: str, receiver: str, message: str) -> None:
        """
        Simulates sending a message between processes.

        Args:
            sender (str): The ID of the sending process.
            receiver (str): The ID of the receiving process.
            message (str): The content of the message.
        """
        logger.debug(f"Sending message from {sender} to {receiver}: {message}")
        self.channels.setdefault(receiver, []).append(message)
        logger.info(f"Message sent from {sender} to {receiver}: {message}")
        logger.debug(f"Updated channels state: {self.channels}")

    def capture_snapshot(self, process_id: str) -> None:
        """
        Captures the state of a process and the messages it has received.

        Args:
            process_id (str): The ID of the process to capture.
        """
        logger.debug(f"Capturing snapshot for process {process_id}.")
        received_messages = self.channels.get(process_id, [])
        snapshot = {
            "received_messages": received_messages.copy(),
            "state": f"State of {process_id}",  # Placeholder for actual state capture.
        }
        self.snapshots[process_id] = snapshot
        logger.info(f"Snapshot captured for process {process_id}.")
        logger.debug(f"Snapshot details: {snapshot}")
        logger.debug(f"Updated snapshots state: {self.snapshots}")

    def get_snapshot(self, process_id: str) -> Optional[dict[str, list[str] | str]]:
        """
        Retrieves the snapshot of a specific process.

        Args:
            process_id (str): The ID of the process whose snapshot is needed.

        Returns:
            dict[str, list[str] | str] | None: The snapshot of the process, or None if not available.
        """
        logger.debug(f"Retrieving snapshot for process {process_id}.")
        snapshot = self.snapshots.get(process_id)
        if snapshot:
            logger.info(f"Snapshot retrieved for process {process_id}: {snapshot}")
        else:
            logger.warning(f"No snapshot found for process {process_id}.")
        return snapshot


if __name__ == "__main__":
    logger.info("Starting Chandy-Lamport example system.")

    system = ChandyLamport()

    logger.info("Sending message from process A to process B.")
    system.send_message("A", "B", "Message 1")

    logger.info("Capturing snapshot for process A.")
    system.capture_snapshot("A")

    logger.info("Capturing snapshot for process B.")
    system.capture_snapshot("B")

    logger.info("Retrieving and printing all snapshots.")
    for process_id in ["A", "B"]:
        snapshot = system.get_snapshot(process_id)
        logger.debug(f"Process {process_id} snapshot: {snapshot}")
