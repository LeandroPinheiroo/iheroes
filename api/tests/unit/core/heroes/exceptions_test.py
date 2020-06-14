import pytest

from iheroes_api.core.heroes.exceptions import HeroNotUniqueError


@pytest.mark.unit
def test_email_not_unique_error():
    user_id = 1
    name = "Bruce Wayne"
    nickname = "Batman"

    error = HeroNotUniqueError(user_id, name, nickname)

    assert error.as_dict() == {
        "msg": "hero already exists",
        "user_id": user_id,
        "hero_name": name,
        "hero_nickname": nickname,
    }

    with pytest.raises(HeroNotUniqueError):
        raise error
