from datetime import datetime

from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.types import JSON, DateTime, Integer

from iheroes_api.infra.database.models import DangerLevelEnum, Threat
from iheroes_api.infra.database.sqlalchemy import metadata

ThreatRecord = Table(
    "threat_record",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("threat_id", Integer, ForeignKey(Threat.c.id), nullable=False),
    Column("danger_level", DangerLevelEnum, nullable=False),
    Column("location", JSON, nullable=False),
    Column(
        "created_at",
        DateTime,
        default=datetime.now,
        server_default=text("NOW()"),
        nullable=False,
    ),
)
