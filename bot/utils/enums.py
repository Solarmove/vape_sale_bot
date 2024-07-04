from enum import Enum
from typing import NamedTuple


class TransactionStatus(Enum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    