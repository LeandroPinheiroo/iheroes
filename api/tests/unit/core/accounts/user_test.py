from functools import partial

import pytest
from pydantic import ValidationError

from iheroes_api.core.accounts.user import Credentials, User, UserRegistry
from tests.utils.asserts import assert_validation_error


@pytest.fixture(name="credentials_valid_data")
def credentials_valid_data_fixture():
    return {
        "email": "example@example.com",
        "password": "some password",
    }


@pytest.fixture(name="credentials_invalid_data")
def credentials_invalid_data_fixture():
    return {
        "email": "some email",
        "password_hash": ["some_hash"],
    }


@pytest.fixture(name="user_valid_data")
def user_valid_data_fixture():
    return {
        "id": 1,
        "email": "example@example.com",
        "password_hash": """
            $argon2i$v=19$m=512,t=2,p=2$aI2R0hpDyLm3ltLa+1/rvQ$LqPKjd6n8yniKtAithoR7A
        """,
    }


@pytest.fixture(name="user_invalid_data")
def user_invalid_data_fixture():
    return {
        "id": "some string",
        "email": "some email",
        "password_hash": ["some_hash"],
    }


@pytest.fixture(name="registry_valid_data")
def registry_valid_data_fixture():
    return {
        "id": 1,
        "email": "example@example.com",
    }


@pytest.fixture(name="registry_invalid_data")
def registry_invalid_data_fixture():
    return {
        "id": "some id",
        "email": "some email",
    }


# Credentials
@pytest.mark.unit
class TestCredentials:
    class TestModel:
        def test_validation(self, credentials_valid_data):
            assert Credentials(**credentials_valid_data)

        def test_invalidation(self, credentials_invalid_data):
            with pytest.raises(ValidationError):
                assert Credentials(**credentials_invalid_data)

        def test_immutability(self, credentials_valid_data):
            entity = Credentials(**credentials_valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, credentials_valid_data):
            credentials_valid_data.update({"email": ["some string"]})
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, credentials_valid_data):
            credentials_valid_data.pop("email")
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPassword:
        assert_validation_error = partial(assert_validation_error, 1, "password")

        def test_must_be_secret_str(self, credentials_valid_data):
            credentials_valid_data.update({"password": ["some string"]})
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, credentials_valid_data):
            credentials_valid_data.pop("password")
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

        def test_min_length_gte_8(self, credentials_valid_data):
            credentials_valid_data.update({"password": "a" * 7})
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length_lte_128(self, credentials_valid_data):
            credentials_valid_data.update({"password": "a" * 129})
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**credentials_valid_data)

            self.assert_validation_error("value_error.any_str.max_length", excinfo)


# User
@pytest.mark.unit
class TestUser:
    class TestModel:
        def test_validation(self, user_valid_data):
            assert User(**user_valid_data)

        def test_invalidation(self, user_invalid_data):
            with pytest.raises(ValidationError):
                assert User(**user_invalid_data)

        def test_immutability(self, user_valid_data):
            entity = User(**user_valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, user_valid_data):
            user_valid_data.update({"id": "some_id"})
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, user_valid_data):
            user_valid_data.pop("id")
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, user_valid_data):
            user_valid_data.update({"email": ["some string"]})
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, user_valid_data):
            user_valid_data.pop("email")
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPasswordHash:
        assert_validation_error = partial(assert_validation_error, 1, "password_hash")

        def test_must_be_secret_str(self, user_valid_data):
            user_valid_data.update({"password_hash": ["some string"]})
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, user_valid_data):
            user_valid_data.pop("password_hash")
            with pytest.raises(ValidationError) as excinfo:
                User(**user_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestUserRegistry:
    class TestModel:
        def test_validation(self, registry_valid_data):
            assert UserRegistry(**registry_valid_data)

        def test_invalidation(self, registry_invalid_data):
            with pytest.raises(ValidationError):
                assert UserRegistry(**registry_invalid_data)

        def test_immutability(self, registry_valid_data):
            entity = UserRegistry(**registry_valid_data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, registry_valid_data):
            registry_valid_data.update({"id": "some_id"})
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**registry_valid_data)

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, registry_valid_data):
            registry_valid_data.pop("id")
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**registry_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        def test_must_be_email(self, registry_valid_data):
            registry_valid_data.update({"email": ["some string"]})
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**registry_valid_data)

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, registry_valid_data):
            registry_valid_data.pop("email")
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**registry_valid_data)

            self.assert_validation_error("value_error.missing", excinfo)
