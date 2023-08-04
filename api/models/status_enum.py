"""
This module contains the Status enum.
"""
from enum import Enum, unique


@unique
class Status(Enum):
    """
    Enumeration representing the status of a bid.

    Each status value represents a different state of a bid in the system.

    Enum Values:
        DELETED (str): The bid has been deleted.
        IN_PROGRESS (str): The bid is currently in progress.
        COMPLETED (str): The bid has been completed.
    """

    DELETED = "deleted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
