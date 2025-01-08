from typing import List
from loguru import logger


class Participant:
    def __init__(self, name: str, vote: bool = True):
        """
        Represents a participant in the two-phase commit protocol.

        Args:
            name (str): The name of the participant.
            vote (bool): Whether this participant agrees to prepare for the transaction.
        """
        self.name = name
        self.vote = vote

    def prepare(self) -> bool:
        """
        Simulates the prepare phase.

        Returns:
            bool: True if the participant is ready to commit, False otherwise.
        """
        response = self.vote
        logger.info(f"Participant {self.name} {'is ready' if response else 'is not ready'} to prepare.")
        return response

    def commit(self) -> None:
        """
        Simulates the commit phase.
        """
        logger.success(f"Participant {self.name} is committing the transaction.")


class TwoPhaseCommit:
    def __init__(self):
        """
        Manages the two-phase commit protocol.
        """
        self.participants: List[Participant] = []
        self.transaction_status: str = "not started"
        logger.info("Initialized TwoPhaseCommit protocol.")

    def add_participant(self, participant: Participant) -> None:
        """
        Adds a participant to the protocol.

        Args:
            participant (Participant): The participant to be added.
        """
        self.participants.append(participant)
        logger.info(f"Added participant {participant.name}.")

    def prepare(self) -> None:
        """
        Executes the two-phase commit protocol.
        """
        if not self.participants:
            logger.warning("No participants to prepare the transaction.")
            self.transaction_status = "aborted"
            return

        # Phase 1: Prepare
        logger.info("Phase 1: Sending prepare request to all participants.")
        all_ready = True

        for participant in self.participants:
            if not participant.prepare():
                all_ready = False
                logger.warning(f"Participant {participant.name} is not ready. Aborting transaction.")
                break

        # Phase 2: Commit or Abort
        if all_ready:
            self.transaction_status = "prepared"
            logger.info("Phase 2: All participants are prepared. Sending commit command.")
            for participant in self.participants:
                participant.commit()
            self.transaction_status = "committed"
            logger.success("Transaction committed successfully.")
        else:
            self.transaction_status = "aborted"
            logger.error("Phase 2: Transaction aborted due to participant readiness failure.")

        logger.info(f"Final transaction status: {self.transaction_status}.")


if __name__ == "__main__":
    logger.info("Starting two-phase commit protocol test.")

    # Initialize the commit protocol
    commit_protocol = TwoPhaseCommit()

    # Add participants with varying readiness
    participant1 = Participant(name="Participant 1", vote=True)
    participant2 = Participant(name="Participant 2", vote=False)  # Simulates a failure change to False
    participant3 = Participant(name="Participant 3", vote=True)

    commit_protocol.add_participant(participant1)
    commit_protocol.add_participant(participant2)
    commit_protocol.add_participant(participant3)

    # Execute the two-phase commit protocol
    commit_protocol.prepare()
