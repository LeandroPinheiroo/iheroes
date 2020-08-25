from typing import Optional

from toolz import assoc

from iheroes_api.core.threats.exceptions import (
    ThreatMonitoredError,
    ThreatNotFoundError,
)
from iheroes_api.core.threats.occurrence import State
from iheroes_api.core.threats.threat import (
    ReportThreatDto,
    Threat,
    ThreatHistory,
    ThreatRecord,
)
from iheroes_api.infra.database.models import Occurrence as OccurrenceModel
from iheroes_api.infra.database.models import Threat as ThreatModel
from iheroes_api.infra.database.models import ThreatRecord as ThreatRecordModel
from iheroes_api.infra.database.sqlalchemy import database


async def create_pending_occurrence(threat: Threat) -> Threat:
    if threat.is_being_monitored():
        raise ThreatMonitoredError(threat)

    initial_state = State.PENDING
    query = OccurrenceModel.insert().values(threat_id=threat.id, state=initial_state)

    await database.execute(query)
    return await fetch_or_raise(threat.id)


async def fetch_by_name(threat_name: str) -> Optional[Threat]:
    query = ThreatModel.select().where(ThreatModel.c.name == threat_name)
    threat = await database.fetch_one(query)

    if not threat:
        return None

    query = OccurrenceModel.select().where(OccurrenceModel.c.threat_id == threat["id"])
    occurrences = await database.fetch_all(query)

    return Threat.parse_obj(assoc(dict(threat), "occurrences", occurrences))


async def fetch_or_raise(threat_id: int) -> Threat:
    query = ThreatModel.select().where(ThreatModel.c.id == threat_id)
    threat = await database.fetch_one(query)

    if not threat:
        raise ThreatNotFoundError()

    query = OccurrenceModel.select().where(OccurrenceModel.c.threat_id == threat_id)
    occurrences = await database.fetch_all(query)

    return Threat.parse_obj(assoc(dict(threat), "occurrences", occurrences))


async def fetch_history(threat_id: int) -> Optional[ThreatHistory]:
    query = (
        ThreatRecordModel.select()
        .where(ThreatRecordModel.c.threat_id == threat_id)
        .order_by(ThreatRecordModel.c.created_at)
    )
    results = await database.fetch_all(query)

    if not results:
        return None

    return ThreatHistory(
        threat_id=threat_id,
        records=[ThreatRecord.parse_obj(record) for record in results],
    )


async def fetch_history_or_raise(threat_id: int) -> ThreatHistory:
    history = await fetch_history(threat_id)
    if not history:
        raise ThreatNotFoundError()
    return history


async def register_history_change(threat_id, dto: ReportThreatDto) -> ThreatHistory:
    values = assoc(dto.dict(exclude={"name"}), "threat_id", threat_id)
    query = ThreatRecordModel.insert().values(**values)
    await database.execute(query)
    return await fetch_history_or_raise(threat_id)


async def upsert(dto: ReportThreatDto) -> Threat:
    threat = await fetch_by_name(dto.name)

    if threat:
        # Update
        values = dto.dict(exclude={"name"})
        query = (
            ThreatModel.update().where(ThreatModel.c.id == threat.id).values(**values)
        )
        await database.execute(query)
        await register_history_change(threat.id, dto)
        return await fetch_or_raise(threat.id)
    else:
        # Create
        values = dto.dict()
        query = ThreatModel.insert().values(**values)
        last_record_id = await database.execute(query)
        await register_history_change(last_record_id, dto)
        return Threat.parse_obj({**values, "id": last_record_id, "occurrences": ()})
