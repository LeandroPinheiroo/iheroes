from sqlalchemy import func
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import JSON, DateTime, Integer

from iheroes_api.infra.database.models.enums import DangerLevelEnum
from iheroes_api.infra.database.models.threat import Threat
from iheroes_api.infra.database.sqlalchemy import metadata

ThreatRecord = Table(
    "threat_record",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "threat_id",
        Integer,
        ForeignKey(Threat.c.id),  # type: ignore[has-type]
        nullable=False,
    ),
    Column("danger_level", DangerLevelEnum, nullable=False),
    Column("location", JSON, nullable=False),
    Column(
        "created_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
)
