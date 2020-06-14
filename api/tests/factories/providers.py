from faker import Faker
from faker.providers import BaseProvider
from passlib.hash import argon2

from iheroes_api.core.heroes.hero import Location

fake = Faker()


class LocationProvider(BaseProvider):
    def location(self) -> Location:
        lat, lng = fake.latlng()
        return Location(lat=float(lat), lng=float(lng))


class PasswordHashProvider(BaseProvider):
    def password_hash(self) -> str:
        return str(argon2.hash(fake.pystr()))
