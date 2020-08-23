from enum import Enum
from operator import itemgetter
from typing import Iterable, Tuple

from pydantic import BaseModel, validator
from toolz import last

from iheroes_api.core.common.location import Location
from iheroes_api.core.threats.occurrence import Occurrence, State


# Enums
class DangerLevel(str, Enum):
    WOLF = "wolf"
    TIGER = "tiger"
    DRAGON = "dragon"
    GOD = "god"


# Entities
class Threat(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    name: str
    danger_level: DangerLevel
    location: Location
    occurrences: Tuple[Occurrence, ...]

    @validator("occurrences", pre=True, always=True)
    def sort_occurrences(
        cls, v: Iterable[Occurrence],  # noqa: N805
    ) -> Iterable[Occurrence]:
        return sorted(v, key=itemgetter("updated_at"))

    @validator("occurrences")
    def validate_occurrences(
        cls, v: Iterable[Occurrence],  # noqa: N805
    ) -> Iterable[Occurrence]:
        monitored_states = [State.PENDING, State.ACTIVE]
        count = [occ for occ in v if occ.state in monitored_states]

        if len(count) > 1:
            raise ValueError("threat has more than one monitored state")
        return v

    def is_being_monitored(self) -> bool:
        if len(self.occurrences) == 0:
            return False

        last_occurrence = last(self.occurrences)
        return False if last_occurrence.state == State.RESOLVED else True


class ThreatRecord(BaseModel):
    class Config:
        allow_mutation = False

    danger_level: DangerLevel
    location: Location


class ThreatHistory(BaseModel):
    class Config:
        allow_mutation = False

    threat_id: int
    records: Tuple[ThreatRecord, ...]


# DTOs
class ReportThreatDto(BaseModel):
    class Config:
        allow_mutation = False

    name: str
    danger_level: DangerLevel
    location: Location
