from enum import Enum

from pydantic import BaseModel

from iheroes_api.core.common.location import Location


class DangerLevel(str, Enum):
    WOLF = "wolf"
    TIGER = "tiger"
    DRAGON = "dragon"
    GOD = "god"


class Threat(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    name: str
    danger_level: DangerLevel
    location: Location


# DTOs
class CreateThreatDto(BaseModel):
    class Config:
        allow_mutation = False

    name: str
    danger_level: DangerLevel
    location: Location


class UpdateThreatDto(BaseModel):
    class Config:
        allow_mutation = False

    danger_level: DangerLevel
    location: Location
