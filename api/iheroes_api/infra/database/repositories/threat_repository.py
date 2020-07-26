from typing import Optional

from toolz import assoc

from iheroes_api.core.threats.exceptions import ThreatNotFoundError
from iheroes_api.core.threats.threat import (
    ReportThreatDto,
    Threat,
    ThreatHistory,
    ThreatRecord,
)
from iheroes_api.infra.database.models import Threat as ThreatModel
from iheroes_api.infra.database.models import ThreatRecord as ThreatRecordModel
from iheroes_api.infra.database.sqlalchemy import database


async def fetch_by_name(threat_name: str) -> Optional[Threat]:
    query = ThreatModel.select().where(ThreatModel.c.name == threat_name)

    result = await database.fetch_one(query)
    return Threat.parse_obj(dict(result)) if result else None


async def fetch_or_raise(threat_id: int) -> Threat:
    query = ThreatModel.select().where(ThreatModel.c.id == threat_id)

    result = await database.fetch_one(query)
    if not result:
        raise ThreatNotFoundError()
    return Threat.parse_obj(dict(result))


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
        return Threat.parse_obj({**values, "id": last_record_id})
