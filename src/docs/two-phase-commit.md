# Two-Phase Commit Protocol Documentation

This document describes the implementation of a Two-Phase Commit (2PC) protocol. The 2PC protocol is a distributed transaction coordination protocol used to ensure consistency across multiple participants.

---

## Overview

The Two-Phase Commit protocol involves two main phases:

1. **Prepare Phase**:
   - The coordinator sends a "prepare" request to all participants.
   - Each participant votes to indicate if they are ready to commit the transaction.

2. **Commit/Abort Phase**:
   - If all participants are ready, the coordinator sends a "commit" request, and the transaction is committed.
   - If any participant is not ready, the coordinator sends an "abort" request, and the transaction is aborted.

---

## Implementation

### `Participant` Class

#### Attributes:
- `name` (`str`): The name of the participant.
- `vote` (`bool`): Indicates the participant's decision to prepare (`True`) or abort (`False`).

#### Methods:
- `prepare() -> bool`: Simulates the participant's decision during the prepare phase. Logs the readiness and returns the participant's vote.
- `commit() -> None`: Simulates the commit phase. Logs the commit action.

### **TwoPhaseCommit Class**

Coordinates the 2PC protocol across all participants.

#### Attributes:
- `participants` (`List[Participant]`): A list of participants involved in the transaction.
- `transaction_status` (`str`): The current status of the transaction (`"not started"`, `"prepared"`, `"committed"`, or `"aborted"`).

#### Methods:
1. **`add_participant(participant: Participant) -> None`**:
   - Adds a participant to the transaction.
   - Logs the addition of the participant.
   - Example log: `Added participant Participant 1.`

2. **`prepare() -> None`**:
   - Executes the Two-Phase Commit protocol:
     - **Phase 1: Prepare**:
       - Sends prepare requests to all participants.
       - Logs participant readiness status.
       - Aborts the transaction if any participant is not ready.
     - **Phase 2: Commit/Abort**:
       - If all participants are ready, sends commit commands and logs success.
       - If any participant is not ready, logs the abort and updates the transaction status.
   - Logs the final transaction status.

---

---

## Usage Example

Below is an example of how to use the `TwoPhaseCommit` protocol:

### Code:

```python
from loguru import logger
from two_phase_commit import TwoPhaseCommit, Participant

# Initialize the 2PC protocol
commit_protocol = TwoPhaseCommit()

# Add participants with their readiness votes
participant1 = Participant(name="Participant 1", vote=True)
participant2 = Participant(name="Participant 2", vote=False)  # Change vote to False to simulate readiness failure
participant3 = Participant(name="Participant 3", vote=True)

commit_protocol.add_participant(participant1)
commit_protocol.add_participant(participant2)
commit_protocol.add_participant(participant3)

# Execute the two-phase commit protocol
commit_protocol.prepare()
```

### Output:
The following steps occur during execution:
1. **Prepare Phase**:
   - Each participant is sent a prepare request:
     - `Participant 1` is ready.
     - `Participant 2` is not ready.
     - `Participant 3` is ready.

2. **Commit/Abort Phase**:
   - If all participants are ready, the transaction is committed.
   - If any participant is not ready, the transaction is aborted.

3. The final transaction status is logged:
   - `"committed"` if all participants are ready.
   - `"aborted"` if any participant is not ready.

---

## Log Messages

- **Info Logs**:
  - Adding participants.
  - Phase transitions (prepare, commit/abort).
  - Individual participant readiness.

- **Warning Logs**:
  - No participants in the protocol.
  - Participant readiness failure.

- **Success Logs**:
  - Transaction committed successfully.

- **Error Logs**:
  - Transaction aborted due to readiness failure.

---

## Advantages and Limitations

### Advantages:
- Guarantees consistency across all participants.
- Participants can abort the transaction if not ready.

### Limitations:
- Requires all participants to be available and responsive.
- Susceptible to blocking if a participant crashes during the protocol.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install loguru
   ```
2. Run the script:
   ```bash
   python src/core/two_phase_commit.py
   ```

---

## Test Cases

1. **All participants are ready**:
   - Expected outcome: Transaction status is `"committed"`.

2. **At least one participant is not ready**:
   - Expected outcome: Transaction status is `"aborted"`.

3. **No participants**:
   - Expected outcome: Transaction status is `"aborted"`. Warning message logged.

---

## Notes

- **Blocking Behavior**: The 2PC protocol can block indefinitely if a participant crashes during the protocol. This is because the coordinator waits for all participants to respond, which can lead to a hang if any participant is unavailable.
  
- **Failure Handling**: The protocol does not currently handle retries or error recovery in case of network failures or participant crashes. Advanced versions of 2PC may implement mechanisms like timeouts or three-phase commit to handle such issues.

- **Consistency Guarantee**: The protocol ensures that either all participants commit the transaction or none do, preserving the consistency of the system. However, it may sacrifice availability in certain scenarios, especially during failures.

- **Scalability**: The 2PC protocol is not particularly scalable for systems with a large number of participants because it requires each participant to be synchronized. Alternative protocols like Paxos or Raft may offer better scalability in highly distributed environments.

---

This implementation provides a robust approach for coordinating distributed transactions in systems where atomicity is critical.