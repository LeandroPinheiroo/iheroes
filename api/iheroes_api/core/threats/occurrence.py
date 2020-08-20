from enum import Enum

from pydantic import BaseModel


# Occurrence
class State(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    RESOLVED = "resolved"


class Occurrence(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    state: State
