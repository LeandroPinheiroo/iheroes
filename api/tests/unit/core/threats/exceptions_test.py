import pytest
from pytest_factoryboy import register
from iheroes_api.core.threats.exceptions import (
    ThreatMonitoredError,
    ThreatNotFoundError,
)
from tests.factories.entity_factories import ThreatFactory

factories = [ThreatFactory]
for factory in factories:
    register(factory)


@pytest.mark.unit
def test_threat_monitored_error(threat_factory):
    id_ = 1
    error = ThreatMonitoredError(threat_factory(id=id_))

    assert error.as_dict() == {
        "type": "threat.already_monitored_error",
        "msg": f"threat id={id_} has monitored occurrence",
    }

    with pytest.raises(ThreatMonitoredError):
        raise error


@pytest.mark.unit
def test_threat_not_found_error():
    error = ThreatNotFoundError()

    assert error.as_dict() == {
        "type": "threat.not_found_error",
        "msg": "threat not found",
    }

    with pytest.raises(ThreatNotFoundError):
        raise error
