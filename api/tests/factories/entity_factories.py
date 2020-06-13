import factory

from iheroes_api.core.accounts.user import Credentials, User, UserRegistry
from tests.factories.providers import PasswordHashProvider

# Register providers
providers = [PasswordHashProvider]
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
