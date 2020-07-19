from enum import Enum
from operator import itemgetter
from typing import List

from pydantic import BaseModel, validator

from iheroes_api.core.common.location import Location
from iheroes_api.core.threats.exceptions import HistoryInvalidEntries


class DangerLevel(str, Enum):
    WOLF = "wolf"
    TIGER = "tiger"
    DRAGON = "dragon"
    GOD = "god"


class ThreatRecord(BaseModel):
    class Config:
        allow_mutation = False

    danger_level: DangerLevel
    location: Location


class Threat(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    name: str
    danger_level: DangerLevel
    location: Location
    history: List[ThreatRecord]

    @validator("history")
    def history_must_contain_latest_entry(cls, v, values):  # noqa: N805
        try:
            danger_level, location = itemgetter("danger_level", "location")(values)
        except KeyError:
            raise HistoryInvalidEntries()

        entries = [
            record
            for record in v
            if record.danger_level == danger_level and record.location == location
        ]
        if not entries:
            raise HistoryInvalidEntries()
        return v


# DTOs
class ReportThreatDto(BaseModel):
    class Config:
        allow_mutation = False

    name: str
    danger_level: DangerLevel
    location: Location
