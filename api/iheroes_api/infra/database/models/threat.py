from sqlalchemy import func
from sqlalchemy.schema import Column, Table
from sqlalchemy.types import JSON, DateTime, Integer, Text

from iheroes_api.infra.database.models import DangerLevelEnum
from iheroes_api.infra.database.sqlalchemy import metadata

Threat = Table(
    "threat",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, unique=True),
    Column("danger_level", DangerLevelEnum, nullable=False),
    Column("location", JSON, nullable=False),
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
        server_onupdate=func.now(),
        nullable=True,
    ),
)
