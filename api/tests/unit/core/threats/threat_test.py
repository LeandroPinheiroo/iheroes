from functools import partial

import pytest
from pydantic import ValidationError
from toolz import dissoc

from iheroes_api.core.threats.threat import (
    CreateThreatDto,
    DangerLevel,
    Threat,
    UpdateThreatDto,
)
from tests.utils.asserts import assert_validation_error


@pytest.fixture(name="valid_threat")
def valid_threat_fixture():
    return {
        "id": 1,
        "name": "Terrorblade",
        "danger_level": "god",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_threat")
def invalid_threat_fixture():
    return {
        "id": "some id",
        "name": ["Doombringer"],
        "danger_level": "Demon",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.fixture(name="valid_create_threat_dto")
def valid_create_threat_dto_fixture():
    return {
        "name": "Davion",
        "danger_level": "dragon",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_create_threat_dto")
def invalid_create_threat_dto_fixture():
    return {
        "name": "Banehallow",
        "danger_level": "hero",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.fixture(name="valid_update_threat_dto")
def valid_update_threat_dto_fixture():
    return {
        "danger_level": "tiger",
        "location": {"lat": 40.6971494, "lng": -74.2598771},
    }


@pytest.fixture(name="invalid_update_threat_dto")
def invalid_update_threat_dto_fixture():
    return {
        "danger_level": "champion",
        "location": {"latitude": "some lat", "longitude": "some lng"},
    }


@pytest.mark.unit
class TestDangerLevel:
    valid = ["wolf", "tiger", "dragon", "god"]

    def test_enum(self):
        for value in self.valid:
            assert DangerLevel(value)

    def test_invalidation(self):
        invalid = ["bronze", "silver", "gold", "platinum"]
        for value in invalid:
            with pytest.raises(
                ValueError, match=f"'{value}' is not a valid DangerLevel"
            ):
                DangerLevel(value)


@pytest.mark.unit
class TestThreat:
    class TestModel:
        def test_validation(self, valid_threat):
            assert Threat(**valid_threat)

        def test_invalidation(self, invalid_threat):
            with pytest.raises(ValidationError):
                Threat(**invalid_threat)

        def test_immutability(self, valid_threat):
            entity = Threat(**valid_threat)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**{**valid_threat, "id": "some_id"})

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**dissoc(valid_threat, "id"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestName:
        assert_validation_error = partial(assert_validation_error, 1, "name")

        def test_must_be_str(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**{**valid_threat, "name": ["Some name"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**dissoc(valid_threat, "name"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestDangerLevel:
        assert_validation_error = partial(assert_validation_error, 1, "danger_level")

        def test_must_be_power_class(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**{**valid_threat, "danger_level": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**dissoc(valid_threat, "danger_level"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_required(self, valid_threat):
            with pytest.raises(ValidationError) as excinfo:
                Threat(**dissoc(valid_threat, "location"))

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestCreateThreatDto:
    class TestModel:
        def test_validation(self, valid_create_threat_dto):
            assert CreateThreatDto(**valid_create_threat_dto)

        def test_invalidation(self, invalid_create_threat_dto):
            with pytest.raises(ValidationError):
                CreateThreatDto(**invalid_create_threat_dto)

        def test_immutability(self, valid_create_threat_dto):
            entity = CreateThreatDto(**valid_create_threat_dto)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestName:
        assert_validation_error = partial(assert_validation_error, 1, "name")

        def test_must_be_str(self, valid_create_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateThreatDto(**{**valid_create_threat_dto, "name": ["Some name"]})

            self.assert_validation_error("type_error.str", excinfo)

        def test_is_required(self, valid_create_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateThreatDto(**dissoc(valid_create_threat_dto, "name"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestDangerLevel:
        assert_validation_error = partial(assert_validation_error, 1, "danger_level")

        def test_must_be_power_class(self, valid_create_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateThreatDto(**{**valid_create_threat_dto, "danger_level": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_create_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateThreatDto(**dissoc(valid_create_threat_dto, "danger_level"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_required(self, valid_create_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                CreateThreatDto(**dissoc(valid_create_threat_dto, "location"))

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
class TestUpdateThreatDto:
    class TestModel:
        def test_validation(self, valid_update_threat_dto):
            assert UpdateThreatDto(**valid_update_threat_dto)

        def test_invalidation(self, invalid_update_threat_dto):
            with pytest.raises(ValidationError):
                UpdateThreatDto(**invalid_update_threat_dto)

        def test_immutability(self, valid_update_threat_dto):
            entity = UpdateThreatDto(**valid_update_threat_dto)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestDangerLevel:
        assert_validation_error = partial(assert_validation_error, 1, "danger_level")

        def test_must_be_power_class(self, valid_update_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateThreatDto(**{**valid_update_threat_dto, "danger_level": 9000})

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_update_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateThreatDto(**dissoc(valid_update_threat_dto, "danger_level"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestLocation:
        assert_validation_error = partial(assert_validation_error, 1, "location")

        def test_is_required(self, valid_update_threat_dto):
            with pytest.raises(ValidationError) as excinfo:
                UpdateThreatDto(**dissoc(valid_update_threat_dto, "location"))

            self.assert_validation_error("value_error.missing", excinfo)
