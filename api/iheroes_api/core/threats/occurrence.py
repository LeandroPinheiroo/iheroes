from enum import Enum
from datetime import datetime
from pydantic import BaseModel


# Enums
class State(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    RESOLVED = "resolved"


# Entities
class Occurrence(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    state: State
    created_at: datetime
    updated_at: datetime
