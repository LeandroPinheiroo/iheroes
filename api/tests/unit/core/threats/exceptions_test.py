import pytest

from iheroes_api.core.threats.exceptions import ThreatNotFoundError


@pytest.mark.unit
def test_threat_not_found_error():
    error = ThreatNotFoundError()

    assert error.as_dict() == {
        "type": "threat.not_found_error",
        "msg": "threat not found",
    }

    with pytest.raises(ThreatNotFoundError):
        raise error
