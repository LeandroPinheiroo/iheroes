import pytest

from iheroes_api.core.heroes.exceptions import HeroNotUniqueError


@pytest.mark.unit
def test_email_not_unique_error():
    error = HeroNotUniqueError()

    assert error.as_dict() == {
        "type": "conflict_error.not_unique",
        "msg": "hero already exists",
    }

    with pytest.raises(HeroNotUniqueError):
        raise error
