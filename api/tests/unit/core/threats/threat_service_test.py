import pytest
from pytest_factoryboy import register

from iheroes_api.core.protocols import ThreatRepo
from iheroes_api.core.threats import threat_service
from tests.factories.entity_factories import ReportThreatDtoFactory, ThreatFactory

factories = [ReportThreatDtoFactory, ThreatFactory]

for factory in factories:
    register(factory)


@pytest.fixture(name="make_threat")
def threat_fixture(threat_factory):
    return lambda **override: threat_factory(**override)


@pytest.fixture(name="make_report_dto")
def report_dto_fixture(report_threat_dto_factory):
    return lambda **override: report_threat_dto_factory(**override)


@pytest.fixture(name="threat_repo")
def threat_repo_fixture(mock_module):
    return mock_module("threat_repo", ThreatRepo)


@pytest.mark.unit
@pytest.mark.asyncio
class TestReportThreat:
    async def test_new_threat(self, threat_repo, make_threat, make_report_dto):
        dto = make_report_dto()
        threat = make_threat(
            name=dto.name, danger_level=dto.danger_level, location=dto.location
        )
        threat_repo.upsert.return_value = threat

        result = await threat_service.report_threat(threat_repo, dto)

        threat_repo.upsert.assert_called_once_with(dto)
        assert result == threat

    async def test_existing_threat(self, threat_repo, make_threat, make_report_dto):
        name = "Darkterror"
        dto = make_report_dto(name=name)
        threat = make_threat(
            name=name,
            danger_level=dto.danger_level,
            location=dto.location,
            history=[
                {"danger_level": "god", "location": {"lat": 10.0, "lng": 20.0}},
                {"danger_level": dto.danger_level, "location": dto.location},
            ],
        )
        threat_repo.upsert.return_value = threat

        result = await threat_service.report_threat(threat_repo, dto)

        threat_repo.upsert.assert_called_once_with(dto)
        assert result == threat
