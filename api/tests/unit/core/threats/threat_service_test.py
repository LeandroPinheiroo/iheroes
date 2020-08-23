import pytest
from pytest_factoryboy import register
from toolz import assoc

from iheroes_api.core.protocols import ThreatMonitor, ThreatRepo
from iheroes_api.core.threats import threat_service
from tests.factories.entity_factories import (
    OccurrenceFactory,
    ReportThreatDtoFactory,
    ThreatFactory,
)

factories = [
    OccurrenceFactory,
    ReportThreatDtoFactory,
    ThreatFactory,
]

for factory in factories:
    register(factory)


@pytest.fixture(name="threat_monitor")
def threat_monitor_fixture(mock_module):
    return mock_module("threat_monitor", ThreatMonitor)


@pytest.fixture(name="threat_repo")
def threat_repo_fixture(mock_module):
    return mock_module("threat_repo", ThreatRepo)


@pytest.mark.unit
@pytest.mark.asyncio
class TestReportThreat:
    async def test_unmonitored_threat(
        self,
        threat_monitor,
        threat_repo,
        occurrence_factory,
        threat_factory,
        report_threat_dto_factory,
    ):
        dto = report_threat_dto_factory()
        threat = threat_factory(
            name=dto.name,
            danger_level=dto.danger_level,
            location=dto.location,
            occurrences=[occurrence_factory(state="resolved").dict()],
        )
        new_threat = threat_factory(
            **assoc(
                threat.dict(),
                "occurrences",
                [occurrence_factory(state="pending").dict()],
            ),
        )

        threat_repo.upsert.return_value = threat
        threat_repo.create_pending_occurrence.return_value = new_threat
        threat_monitor.start_monitoring.return_value = new_threat

        result = await threat_service.report_threat(threat_monitor, threat_repo, dto)

        threat_repo.upsert.assert_called_once_with(dto)
        threat_repo.create_pending_occurrence.assert_called_once_with(threat)
        threat_monitor.start_monitoring.assert_called_once_with(new_threat)

        assert result == new_threat
        assert result.is_being_monitored() is True

    async def test_monitored_threat(
        self,
        threat_monitor,
        threat_repo,
        occurrence_factory,
        threat_factory,
        report_threat_dto_factory,
    ):
        name = "Darkterror"
        dto = report_threat_dto_factory(name=name)
        threat = threat_factory(
            name=name,
            danger_level=dto.danger_level,
            location=dto.location,
            occurrences=[occurrence_factory(state="pending").dict()],
        )

        threat_repo.upsert.return_value = threat

        result = await threat_service.report_threat(threat_monitor, threat_repo, dto)

        threat_repo.upsert.assert_called_once_with(dto)
        assert not threat_repo.create_pending_occurrence.called
        assert not threat_monitor.start_monitoring.called
        assert result == threat
        assert result.is_being_monitored() is True
