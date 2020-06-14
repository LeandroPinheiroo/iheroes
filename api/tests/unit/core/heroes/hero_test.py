from functools import partial
from string import ascii_lowercase, ascii_uppercase

import pytest
from pydantic import ValidationError
from toolz.dicttoolz import dissoc

from iheroes_api.core.heroes.hero import (
    CreateHeroDto,
    Hero,
    Location,
    PowerClass,
    UpdateHeroDto,
)
from tests.utils.asserts import assert_validation_error


@pytest.fixture(name="valid_location")
def valid_location_fixture():
    return {
        "lat": 38.8935128,
        "lng": -77.1546632,
    }


@pytest.fixture(name="invalid_location")
def invalid_location_fixture():
    return {
        "lat": "some float",
        "lng": "some float",
    }


@pytest.fixture(name="valid_hero")
def valid_hero_fixture():
    return {
        "id": 1,
        "user_id": 2,
        "name": "Bruce Wayne",
        "nickname": "Batman",
        "power_class": "B",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_hero")
def invalid_hero_fixture():
    return {
        "id": "some id",
        "user_id": "some user_id",
        "name": ["Bruce Wayne"],
        "nickname": ["Batman"],
        "power_class": "X",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.fixture(name="valid_create_hero_dto")
def valid_create_hero_dto_fixture():
    return {
        "name": "Bruce Wayne",
        "nickname": "Batman",
        "power_class": "B",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_create_hero_dto")
def invalid_create_hero_dto_fixture():
    return {
        "name": ["Bruce Wayne"],
        "nickname": ["Batman"],
        "power_class": "X",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.fixture(name="valid_update_hero_dto")
def valid_update_hero_dto_fixture():
    return {
        "name": "Bruce Wayne",
        "nickname": "Batman",
        "power_class": "B",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_update_hero_dto")
def invalid_update_hero_dto_fixture():
    return {
        "name": ["Bruce Wayne"],
        "nickname": ["Batman"],
        "power_class": "X",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.mark.unit
class TestPowerClass:
    valid = ["S", "A", "B", "C"]

    def test_enum(self):
        for value in self.valid:
            assert PowerClass(value)

    def test_invalidation(self):
        invalid = set(ascii_lowercase).union(ascii_uppercase).difference(self.valid)
        for value in invalid:
            with pytest.raises(
                ValueError, match=f"'{value}' is not a valid PowerClass"
            ):
                PowerClass(value)


@pytest.mark.unit
class TestLocation:
    class TestModel:
        def test_validation(self, valid_location):
            assert Location(**valid_location)

        def test_invalidation(self, invalid_location):
            with pytest.raises(ValidationError):
                Location(**invalid_location)

        def test_immutability(self, valid_location):
            entity = Location(**valid_location)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestLat:
        assert_validation_error = partial(assert_validation_error, 1, "lat")

        def test_must_be_float(self, valid_location):
            with pytest.raises(ValidationError) as excinfo:
                Location(**{**valid_location, "lat": "some float"})

            self.assert_validation_error("type_error.float", excinfo)

        def test_is_required(self, valid_location):
            with pytest.raises(ValidationError) as excinfo:
                Location(**dissoc(valid_location, "lat"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLng:
        assert_validation_error = partial(assert_validation_error, 1, "lng")

        def test_must_be_float(self, valid_location):
            with pytest.raises(ValidationError) as excinfo:
                Location(**{**valid_location, "lng": "some float"})

            self.assert_validation_error("type_error.float", excinfo)

        def test_is_required(self, valid_location):
            with pytest.raises(ValidationError) as excinfo:
                Location(**dissoc(valid_location, "lng"))

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestHero:
    class TestModel:
        def test_validation(self, valid_hero):
            assert Hero(**valid_hero)

        def test_invalidation(self, invalid_hero):
            with pytest.raises(ValidationError):
                Hero(**invalid_hero)

        def test_immutability(self, valid_hero):
            entity = Hero(**valid_hero)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "id": "some_id"})

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**dissoc(valid_hero, "id"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestUserId:
        assert_validation_error = partial(assert_validation_error, 1, "user_id")

        def test_must_be_int(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "user_id": "some_id"})

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**dissoc(valid_hero, "user_id"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestName:
        assert_validation_error = partial(assert_validation_error, 1, "name")

        def test_must_be_str(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "name": ["Some name"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_defaults(self, valid_hero):
            assert Hero(**dissoc(valid_hero, "name")).name == "Unknown"

        def test_min_length(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "name": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "name": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestNickname:
        assert_validation_error = partial(assert_validation_error, 1, "nickname")

        def test_must_be_str(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "nickname": ["Some nickname"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**dissoc(valid_hero, "nickname"))

            self.assert_validation_error("value_error.missing", excinfo)

        def test_min_length(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "nickname": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "nickname": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestPowerClass:
        assert_validation_error = partial(assert_validation_error, 1, "power_class")

        def test_must_be_power_class(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**{**valid_hero, "power_class": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**dissoc(valid_hero, "power_class"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_required(self, valid_hero):
            with pytest.raises(ValidationError) as excinfo:
                Hero(**dissoc(valid_hero, "location"))

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestCreateHeroDto:
    class TestModel:
        def test_validation(self, valid_create_hero_dto):
            assert CreateHeroDto(**valid_create_hero_dto)

        def test_invalidation(self, invalid_create_hero_dto):
            with pytest.raises(ValidationError):
                CreateHeroDto(**invalid_create_hero_dto)

        def test_immutability(self, valid_create_hero_dto):
            entity = CreateHeroDto(**valid_create_hero_dto)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestName:
        assert_validation_error = partial(assert_validation_error, 1, "name")

        def test_must_be_str(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "name": ["Some name"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_defaults(self, valid_create_hero_dto):
            assert (
                CreateHeroDto(**dissoc(valid_create_hero_dto, "name")).name == "Unknown"
            )

        def test_min_length(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "name": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "name": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestNickname:
        assert_validation_error = partial(assert_validation_error, 1, "nickname")

        def test_must_be_str(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(
                    **{**valid_create_hero_dto, "nickname": ["Some nickname"]}
                )

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**dissoc(valid_create_hero_dto, "nickname"))

            self.assert_validation_error("value_error.missing", excinfo)

        def test_min_length(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "nickname": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "nickname": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestPowerClass:
        assert_validation_error = partial(assert_validation_error, 1, "power_class")

        def test_must_be_power_class(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**{**valid_create_hero_dto, "power_class": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**dissoc(valid_create_hero_dto, "power_class"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_required(self, valid_create_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateHeroDto(**dissoc(valid_create_hero_dto, "location"))

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestUpdateHeroDto:
    class TestModel:
        def test_validation(self, valid_update_hero_dto):
            assert UpdateHeroDto(**valid_update_hero_dto)

        def test_invalidation(self, invalid_update_hero_dto):
            with pytest.raises(ValidationError):
                UpdateHeroDto(**invalid_update_hero_dto)

        def test_immutability(self, valid_update_hero_dto):
            entity = UpdateHeroDto(**valid_update_hero_dto)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestName:
        assert_validation_error = partial(assert_validation_error, 1, "name")

        def test_must_be_str(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "name": ["Some name"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_defaults(self, valid_update_hero_dto):
            assert (
                UpdateHeroDto(**dissoc(valid_update_hero_dto, "name")).name == "Unknown"
            )

        def test_min_length(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "name": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "name": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestNickname:
        assert_validation_error = partial(assert_validation_error, 1, "nickname")

        def test_must_be_str(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(
                    **{**valid_update_hero_dto, "nickname": ["Some nickname"]}
                )

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_optional(self, valid_update_hero_dto):
            assert UpdateHeroDto(**dissoc(valid_update_hero_dto, "nickname"))

        def test_min_length(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "nickname": ""})

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        def test_max_length(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "nickname": "a" * 101})

            self.assert_validation_error("value_error.any_str.max_length", excinfo)

    class TestPowerClass:
        assert_validation_error = partial(assert_validation_error, 1, "power_class")

        def test_must_be_power_class(self, valid_update_hero_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateHeroDto(**{**valid_update_hero_dto, "power_class": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_optional(self, valid_update_hero_dto):
            assert UpdateHeroDto(**dissoc(valid_update_hero_dto, "power_class"))

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_optional(self, valid_update_hero_dto):
            assert UpdateHeroDto(**dissoc(valid_update_hero_dto, "location"))
