from enum import Enum
from typing import List

from pydantic import BaseModel

from iheroes_api.core.common.location import Location


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


class ThreatRecord(BaseModel):
    class Config:
        allow_mutation = False

    danger_level: DangerLevel
    location: Location


class ThreatHistory(BaseModel):
    class Config:
        allow_mutation = False

    threat_id: int
    records: List[ThreatRecord]


# DTOs
class ReportThreatDto(BaseModel):
    class Config:
        allow_mutation = False

    name: str
    danger_level: DangerLevel
    location: Location
