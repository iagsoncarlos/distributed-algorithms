from typing import List
from loguru import logger


class Participant:
    def __init__(self, name: str, vote: bool = True):
        """
        Represents a participant in the one-phase commit protocol.

        Args:
            name (str): The name of the participant.
            vote (bool): Whether this participant agrees to commit the transaction.
        """
        self.name = name
        self.vote = vote

    def vote_commit(self) -> bool:
        """
        Simulates the voting process for the commit.

        Returns:
            bool: True if the participant votes to commit, False otherwise.
        """
        logger.info(f"Participant {self.name} votes {'commit' if self.vote else 'abort'}.")
        return self.vote


class OnePhaseCommit:
    def __init__(self):
        """
        Manages the one-phase commit protocol.
        """
        self.participants: List[Participant] = []
        self.transaction_status: str = "not started"
        logger.info("Initialized OnePhaseCommit protocol.")

    def add_participant(self, participant: Participant) -> None:
        """
        Adds a participant to the protocol.

        Args:
            participant (Participant): The participant to be added.
        """
        self.participants.append(participant)
        logger.info(f"Added participant {participant.name}.")

    def commit(self) -> None:
        """
        Executes the one-phase commit protocol.
        """
        if not self.participants:
            logger.warning("No participants to commit the transaction.")
            self.transaction_status = "aborted"
            return

        # Step 1: Broadcast commit request to all participants
        logger.info("Broadcasting commit request to all participants.")
        all_agreed = True

        for participant in self.participants:
            if not participant.vote_commit():
                all_agreed = False
                logger.warning(f"Participant {participant.name} voted to abort.")
                break

        # Step 2: Decide outcome based on participants' votes
        if all_agreed:
            self.transaction_status = "committed"
            logger.success("Transaction committed successfully.")
        else:
            self.transaction_status = "aborted"
            logger.error("Transaction aborted due to participant disagreement.")

        logger.info(f"Final transaction status: {self.transaction_status}.")


if __name__ == "__main__":
    logger.info("Starting one-phase commit protocol test.")

    # Initialize the commit protocol
    commit_protocol = OnePhaseCommit()

    # Add participants with varying commit votes
    participant1 = Participant(name="Participant 1", vote=True)
    participant2 = Participant(name="Participant 2", vote=True) # Simulates a failure change to False
    participant3 = Participant(name="Participant 3", vote=True)

    commit_protocol.add_participant(participant1)
    commit_protocol.add_participant(participant2)
    commit_protocol.add_participant(participant3)

    # Execute the commit protocol
    commit_protocol.commit()
