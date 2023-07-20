from enum import Enum, unique


# Enum for status
@unique
class Status(Enum):
    DELETED = "deleted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
