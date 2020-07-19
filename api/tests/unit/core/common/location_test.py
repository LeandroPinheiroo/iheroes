from functools import partial

import pytest
from pydantic import ValidationError
from toolz.dicttoolz import dissoc

from iheroes_api.core.common.location import Location
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
