from pydantic import BaseModel


class Location(BaseModel):
    class Config:
        allow_mutation = False

    lat: float
    lng: float
