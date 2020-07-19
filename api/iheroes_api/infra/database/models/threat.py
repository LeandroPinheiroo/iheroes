from datetime import datetime

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.types import JSON, DateTime, Integer, Text

from iheroes_api.infra.database.sqlalchemy import metadata

Threat = Table(
    "threat",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False, unique=True),
    Column(
        "danger_level",
        ENUM("wolf", "tiger", "dragon", "god", name="danger_level"),
        nullable=False,
    ),
    Column("location", JSON, nullable=False),
    Column(
        "created_at",
        DateTime,
        default=datetime.now,
        server_default=text("NOW()"),
        nullable=False,
    ),
    Column("updated_at", DateTime, onupdate=datetime.now, nullable=True),
)
