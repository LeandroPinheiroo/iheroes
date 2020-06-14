import factory

from iheroes_api.core.accounts.user import Credentials, User, UserRegistry
from iheroes_api.core.heroes.hero import CreateHeroDto, Hero, PowerClass, UpdateHeroDto
from tests.factories.providers import LocationProvider, PasswordHashProvider

# Register providers
providers = [LocationProvider, PasswordHashProvider]
for provider in providers:
    factory.Faker.add_provider(provider)


# User
class CredentialsFactory(factory.Factory):
    class Meta:
        model = Credentials

    email = factory.Faker("email")
    password = factory.Faker("password", length=16)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    email = factory.Faker("email")
    password_hash = factory.Faker("password_hash")


class UserRegistryFactory(factory.Factory):
    class Meta:
        model = UserRegistry

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    email = factory.Faker("email")


# Hero
class HeroFactory(factory.Factory):
    class Meta:
        model = Hero

    id = factory.Faker("pyint", min_value=0)  # noqa: A003
    user_id = factory.Faker("pyint", min_value=0)  # noqa: A003
    name = factory.Faker("name")
    nickname = factory.Faker("user_name")
    power_class = factory.Faker(
        "random_element", elements=[e.value for e in PowerClass]
    )
    location = factory.Faker("location")


class CreateHeroDtoFactory(factory.Factory):
    class Meta:
        model = CreateHeroDto

    name = factory.Faker("name")
    nickname = factory.Faker("user_name")
    power_class = factory.Faker(
        "random_element", elements=[e.value for e in PowerClass]
    )
    location = factory.Faker("location")


class UpdateHeroDtoFactory(factory.Factory):
    class Meta:
        model = UpdateHeroDto

    name = factory.Faker("name")
    nickname = factory.Faker("user_name")
    power_class = factory.Faker(
        "random_element", elements=[e.value for e in PowerClass]
    )
    location = factory.Faker("location")
