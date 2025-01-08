# One-Phase Commit Protocol Documentation

This document describes the implementation of a One-Phase Commit (1PC) protocol. The 1PC protocol is a simplified transaction coordination protocol used to determine whether a distributed transaction should be committed or aborted based on the votes of participants.

---

## Overview

The 1PC protocol is designed for scenarios where participants can unanimously agree to commit or abort a transaction. Each participant in the protocol votes independently, and the transaction is committed only if all participants vote to commit. If any participant votes to abort, the transaction is aborted.

---

## Implementation

### `Participant` Class

#### Attributes:
- `name` (`str`): The name of the participant.
- `vote` (`bool`): Indicates the participant's decision to commit (`True`) or abort (`False`).

#### Methods:
- `vote_commit() -> bool`: Simulates the voting process. Logs the participant's vote and returns their decision.

### `OnePhaseCommit` Class

#### Attributes:
- `participants` (`List[Participant]`): A list of participants in the transaction.
- `transaction_status` (`str`): The current status of the transaction (`"not started"`, `"committed"`, `"aborted"`).

#### Methods:
- `add_participant(participant: Participant) -> None`: Adds a participant to the protocol.
- `commit() -> None`: Executes the 1PC protocol. Broadcasts a commit request to all participants, aggregates their votes, and determines the transaction outcome.

---

## Usage Example

Below is an example of how to use the `OnePhaseCommit` protocol:

### Code:

```python
from loguru import logger
from one_phase_commit import OnePhaseCommit, Participant

# Initialize the 1PC protocol
commit_protocol = OnePhaseCommit()

# Add participants with their votes
participant1 = Participant(name="Participant 1", vote=True)
participant2 = Participant(name="Participant 2", vote=True)  # Change vote to False to simulate abort
participant3 = Participant(name="Participant 3", vote=True)

commit_protocol.add_participant(participant1)
commit_protocol.add_participant(participant2)
commit_protocol.add_participant(participant3)

# Execute the commit protocol
commit_protocol.commit()
```

### Output:
The following steps occur during execution:
1. Each participant is asked to vote:
   - `Participant 1` votes commit.
   - `Participant 2` votes commit (or abort if changed to `False`).
   - `Participant 3` votes commit.

2. If all participants vote to commit:
   - Transaction status is updated to `"committed"`.
   - Success message is logged.

3. If any participant votes to abort:
   - Transaction status is updated to `"aborted"`.
   - Error message is logged.

---

## Log Messages

- **Info Logs**:
  - Adding participants.
  - Broadcasting commit request.
  - Individual participant votes.

- **Warning Logs**:
  - No participants in the protocol.
  - Participant votes to abort.

- **Success Logs**:
  - Transaction committed successfully.

- **Error Logs**:
  - Transaction aborted due to participant disagreement.

---

## Advantages and Limitations

### Advantages:
- Simple and easy to implement.
- Suitable for small-scale distributed transactions.

### Limitations:
- Lack of fault tolerance (e.g., network failures or participant crashes).
- Requires all participants to be available and responsive.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install loguru
   ```
2. Run the script:
   ```bash
   python src/core/one_phase_commit.py
   ```

---

## Test Cases

1. **All participants vote to commit**:
   - Expected outcome: Transaction status is `"committed"`.

2. **At least one participant votes to abort**:
   - Expected outcome: Transaction status is `"aborted"`.

3. **No participants**:
   - Expected outcome: Transaction status is `"aborted"`. Warning message logged.

---

## Notes:

- **Fault Tolerance**: The 1PC protocol does not include mechanisms to handle participant failures or network issues during the voting phase. For fault tolerance, more advanced protocols like 2PC should be considered.
  
- **Scalability**: The protocol is suitable for scenarios with a small number of participants, but may not scale well in highly distributed systems where network latency or partitioning could occur.

- **Simplification**: Since all participants must vote simultaneously, this protocol is simple and can be used in environments where it is acceptable to not have advanced failure recovery mechanisms.

- **Transaction Rollback**: If the transaction is aborted, the protocol assumes that all participants will immediately perform a rollback of the transaction, which may need to be explicitly handled depending on the use case.

---

This implementation provides a foundation for exploring distributed transaction coordination in systems with simple requirements.