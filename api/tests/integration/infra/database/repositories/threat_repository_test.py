from operator import attrgetter, itemgetter

import pytest
from pytest_factoryboy import register
from toolz import assoc, dissoc

from iheroes_api.core.threats.exceptions import (
    ThreatMonitoredError,
    ThreatNotFoundError,
)
from iheroes_api.core.threats.occurrence import State
from iheroes_api.infra.database.repositories import threat_repository
from tests.factories.entity_factories import (
    OccurrenceFactory,
    ReportThreatDtoFactory,
    ThreatFactory,
)
from tests.factories.model_factories import insert_threat, insert_threat_record

factories = [OccurrenceFactory, ReportThreatDtoFactory, ThreatFactory]

for factory in factories:
    register(factory)


@pytest.mark.integration
@pytest.mark.asyncio
class TestCreatePendingOccurrence:
    async def test_success(self, database, threat_factory):
        threat = threat_factory()
        insert_threat(threat.dict())

        result = await threat_repository.create_pending_occurrence(threat)
        assert len(result.occurrences) == 1
        assert result.occurrences[0].state == State.PENDING

    async def test_threat_monitored(self, database, threat_factory, occurrence_factory):
        threat = threat_factory(
            occurrences=(occurrence_factory(state="active").dict(),)
        )
        insert_threat(threat.dict())

        with pytest.raises(ThreatMonitoredError):
            await threat_repository.create_pending_occurrence(threat)


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchByName:
    async def test_found(self, database, threat_factory):
        name = "lina"
        threat = threat_factory(name=name, occurrences=())
        insert_threat(threat.dict())

        result = await threat_repository.fetch_by_name(name)
        assert result == threat

    async def test_not_found(self):
        result = await threat_repository.fetch_by_name("lina")
        assert result is None


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchHistory:
    async def test_found(self, database, threat_factory):
        id_ = 1
        threat = threat_factory(id=id_)
        insert_threat(threat.dict())

        record = assoc(dissoc(threat.dict(), "id"), "threat_id", id_)
        insert_threat_record(record)

        result = await threat_repository.fetch_history(id_)

        assert result
        assert result.threat_id == id_

        getter = itemgetter("danger_level", "location")
        assert getter(result.records[0].dict()) == getter(record)

    async def test_not_found(self):
        result = await threat_repository.fetch_history(1)
        assert result is None


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchHistoryOrRaise:
    async def test_found(self, database, threat_factory):
        id_ = 1
        threat = threat_factory(id=id_)
        insert_threat(threat.dict())

        record = assoc(dissoc(threat.dict(), "id"), "threat_id", id_)
        insert_threat_record(record)

        result = await threat_repository.fetch_history_or_raise(id_)

        assert result
        assert result.threat_id == id_

        getter = itemgetter("danger_level", "location")
        assert getter(result.records[0].dict()) == getter(record)

    async def test_not_found(self):
        with pytest.raises(ThreatNotFoundError):
            await threat_repository.fetch_history_or_raise(1)


@pytest.mark.integration
@pytest.mark.asyncio
class TestFetchOrRaise:
    async def test_found(self, database, threat_factory):
        id_ = 1
        threat = threat_factory(id=id_, occurrences=())
        insert_threat(threat.dict())

        result = await threat_repository.fetch_or_raise(id_)
        assert result == threat

    async def test_not_found(self):
        with pytest.raises(ThreatNotFoundError):
            await threat_repository.fetch_or_raise(1)


@pytest.mark.integration
@pytest.mark.asyncio
class TestRegisterHistoryChange:
    async def test_success(self, database, threat_factory, report_threat_dto_factory):
        id_ = 1
        threat = threat_factory(id=id_)
        insert_threat(threat.dict())
        dto = report_threat_dto_factory()

        result = await threat_repository.register_history_change(id_, dto)

        assert result.threat_id == id_

        getter = itemgetter("danger_level", "location")
        assert getter(result.records[0].dict()) == getter(dto.dict())

    async def test_threat_not_found(self, report_threat_dto_factory):
        pass


@pytest.mark.integration
@pytest.mark.asyncio
class TestUpsert:
    async def test_update(self, database, threat_factory, report_threat_dto_factory):
        id_ = 1
        name = "darkterror"
        threat = threat_factory(id=id_, name=name)
        insert_threat(threat.dict())
        insert_threat_record(assoc(dissoc(threat.dict(), "id"), "threat_id", id_))

        dto = report_threat_dto_factory(name=name)
        result = await threat_repository.upsert(dto)

        getter = itemgetter("danger_level", "location")
        assert getter(result.dict()) == getter(dto.dict())
        assert result.name == threat.name

    async def test_insert(self, database, report_threat_dto_factory):
        name = "enigma"
        dto = report_threat_dto_factory(name=name)
        result = await threat_repository.upsert(dto)

        assert result

    async def test_update_record_history(
        self, database, threat_factory, report_threat_dto_factory
    ):
        id_ = 1
        name = "tidehunter"
        threat = threat_factory(id=id_, name=name)
        insert_threat(threat.dict())
        insert_threat_record(assoc(dissoc(threat.dict(), "id"), "threat_id", id_))

        dto = report_threat_dto_factory(name=name)
        await threat_repository.upsert(dto)
        history = await threat_repository.fetch_history_or_raise(id_)

        assert history.threat_id == id_

        getter = attrgetter("danger_level", "location")
        past, present = history.records
        assert getter(past) == getter(threat)
        assert getter(present) == getter(dto)

    async def test_insert_record_history(self, database, report_threat_dto_factory):
        id_ = 1
        dto = report_threat_dto_factory(id=id_)

        threat = await threat_repository.upsert(dto)
        history = await threat_repository.fetch_history_or_raise(id_)

        assert history.threat_id == id_
        getter = attrgetter("danger_level", "location")
        assert getter(threat) == getter(dto)
