import sys
import argparse
import threading
from loguru import logger

from core.mvcc import MVCC
from core.chandy_lamport import ChandyLamport
from core.distributed_lock import Zookeeper, DistributedLock, Worker
from core.one_phase_commit import OnePhaseCommit, Participant as OnePCParticipant
from core.two_phase_commit import TwoPhaseCommit, Participant as TwoPCParticipant

def main():
    parser = argparse.ArgumentParser(description="Run distributed algorithms")
    parser.add_argument(
        "algorithm", choices=["chandy_lamport", "mvcc", "one_phase_commit", "two_phase_commit", "distributed_lock"],
        help="The algorithm to run"
    )
    parser.add_argument(
        "--log", default="info", choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level"
    )
    
    args = parser.parse_args()

    # Set logging level based on argument
    logger.remove()
    logger.add(sys.stdout, level=args.log.upper())

    if args.algorithm == "chandy_lamport":
        logger.info("Running Chandy-Lamport Algorithm")
        system = ChandyLamport()
        system.send_message("A", "B", "Message 1")
        system.capture_snapshot("A")
        system.capture_snapshot("B")
        for process_id in ["A", "B"]:
            snapshot = system.get_snapshot(process_id)
            logger.debug(f"Process {process_id} snapshot: {snapshot}")

    elif args.algorithm == "mvcc":
        logger.info("Running MVCC Algorithm")
        db = MVCC()
        db.begin_transaction(1)
        db.write(1, "key1", "value1")
        logger.info(f"Read key1 in transaction 1: {db.read(1, 'key1')}")
        db.commit(1)
        db.show_data()
        db.begin_transaction(2)
        db.write(2, "key2", "value2")
        logger.info(f"Read key2 in transaction 2: {db.read(2, 'key2')}")
        db.rollback(2)
        logger.info(f"Read key2 after rollback: {db.read(2, 'key2', fallback_to_main=True)}")
        db.show_data()

    elif args.algorithm == "one_phase_commit":
        logger.info("Running One-Phase Commit Algorithm")
        commit_protocol = OnePhaseCommit()
        participant1 = OnePCParticipant(name="Participant 1", vote=True)
        participant2 = OnePCParticipant(name="Participant 2", vote=True)  # Simulates a failure change to False
        participant3 = OnePCParticipant(name="Participant 3", vote=True)
        commit_protocol.add_participant(participant1)
        commit_protocol.add_participant(participant2)
        commit_protocol.add_participant(participant3)
        commit_protocol.commit()

    elif args.algorithm == "two_phase_commit":
        logger.info("Running Two-Phase Commit Algorithm")
        commit_protocol = TwoPhaseCommit()
        participant1 = TwoPCParticipant(name="Participant 1", vote=True)
        participant2 = TwoPCParticipant(name="Participant 2", vote=True)  # Simulates a failure change to False
        participant3 = TwoPCParticipant(name="Participant 3", vote=True)
        commit_protocol.add_participant(participant1)
        commit_protocol.add_participant(participant2)
        commit_protocol.add_participant(participant3)
        commit_protocol.prepare()
        
    elif args.algorithm == "distributed_lock":
        logger.info("Running Distributed Lock Simulation")
        zookeeper = Zookeeper()
        zookeeper.create_node("/distributed_lock", "initial_value")

        threads = []
        for i in range(3):  # Simulate 3 clients attempting to acquire the lock
            lock = DistributedLock(zookeeper, "/distributed_lock", f"Client-{i+1}")
            worker_instance = Worker(lock)  # Instantiate worker with the lock
            t = threading.Thread(target=worker_instance.perform_task)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
