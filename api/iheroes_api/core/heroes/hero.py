from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

# Typedefs
Name = Field("Unknown", min_length=1, max_length=100)
OptionalName = Field("Unknown", min_length=1, max_length=100)
Nickname = Field(..., min_length=1, max_length=100)
OptionalNickname = Field(None, min_length=1, max_length=100)


# Domain entities
class PowerClass(str, Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"


class Location(BaseModel):
    class Config:
        allow_mutation = False

    lat: float
    lng: float


class Hero(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    user_id: int
    name: Optional[str] = Field("Unknown", min_length=1, max_length=100)
    nickname: str = Field(..., min_length=1, max_length=100)
    power_class: PowerClass
    location: Location


# DTOs
class CreateHeroDto(BaseModel):
    class Config:
        allow_mutation = False

    name: Optional[str] = Name
    nickname: str = Nickname
    power_class: PowerClass
    location: Location


class UpdateHeroDto(BaseModel):
    class Config:
        allow_mutation = False

    name: Optional[str] = OptionalName
    nickname: Optional[str] = OptionalNickname
    power_class: Optional[PowerClass]
    location: Optional[Location]
