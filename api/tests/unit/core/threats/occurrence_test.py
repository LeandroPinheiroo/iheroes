from datetime import datetime
from functools import partial

import pytest
from pydantic import ValidationError
from toolz import assoc, dissoc

from iheroes_api.core.threats.occurrence import Occurrence, State
from tests.utils.asserts import assert_validation_error


@pytest.fixture(name="valid_occurrence")
def valid_occurrence_fixture():
    return {
        "id": 1,
        "state": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


@pytest.fixture(name="invalid_occurrence")
def invalid_occurrence_fixture():
    return {
        "id": "some id",
        "state": "some state",
        "created_at": "some datetime",
        "updated_at": "some datetime",
    }


@pytest.mark.unit
class TestDangerLevel:
    valid = ["pending", "active", "resolved"]

    def test_enum(self):
        for value in self.valid:
            assert State(value)

    def test_invalidation(self):
        invalid = ["waiting", "running", "completed"]
        for value in invalid:
            with pytest.raises(ValueError, match=f"'{value}' is not a valid State"):
                State(value)


@pytest.mark.unit
class TestOccurrence:
    class TestModel:
        def test_validation(self, valid_occurrence):
            assert Occurrence(**valid_occurrence)

        def test_invalidation(self, invalid_occurrence):
            with pytest.raises(ValidationError):
                Occurrence(**invalid_occurrence)

        def test_immutability(self, valid_occurrence):
            entity = Occurrence(**valid_occurrence)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        def test_must_be_int(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**assoc(valid_occurrence, "id", "some id"))

            self.assert_validation_error("type_error.integer", excinfo)

        def test_is_required(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**dissoc(valid_occurrence, "id"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestState:
        assert_validation_error = partial(assert_validation_error, 1, "state")

        def test_must_be_state(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**assoc(valid_occurrence, "state", "some state"))

            self.assert_validation_error("type_error.enum", excinfo)

        def test_is_required(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**dissoc(valid_occurrence, "state"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestCreatedAt:
        assert_validation_error = partial(assert_validation_error, 1, "created_at")

        def test_must_be_datetime(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**assoc(valid_occurrence, "created_at", "some datetime"))

            self.assert_validation_error("value_error.datetime", excinfo)

        def test_is_required(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**dissoc(valid_occurrence, "created_at"))

            self.assert_validation_error("value_error.missing", excinfo)

    class TestUpdatedAt:
        assert_validation_error = partial(assert_validation_error, 1, "updated_at")

        def test_must_be_datetime(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**assoc(valid_occurrence, "updated_at", "some datetime"))

            self.assert_validation_error("value_error.datetime", excinfo)

        def test_is_required(self, valid_occurrence):
            with pytest.raises(ValidationError) as excinfo:
                Occurrence(**dissoc(valid_occurrence, "updated_at"))

            self.assert_validation_error("value_error.missing", excinfo)
