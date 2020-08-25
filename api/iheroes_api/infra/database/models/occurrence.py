from sqlalchemy import func
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import DateTime, Integer

from iheroes_api.infra.database.models.enums import OccurrenceStateEnum
from iheroes_api.infra.database.models.threat import Threat
from iheroes_api.infra.database.sqlalchemy import metadata

Occurrence = Table(
    "occurrence",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("threat_id", Integer, ForeignKey(Threat.c.id), nullable=False),
    Column("state", OccurrenceStateEnum, nullable=False),
    Column(
        "created_at",
        DateTime,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        DateTime,
        onupdate=func.now(),
        default=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    ),
)
