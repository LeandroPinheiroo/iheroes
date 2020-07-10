from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    Table,
    UniqueConstraint,
)
from sqlalchemy.types import JSON, Integer, String

from iheroes_api.infra.database.models.user import User
from iheroes_api.infra.database.sqlalchemy import metadata

Hero = Table(
    "hero",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(User.c.id), nullable=False),
    Column(
        "name", String(100), nullable=False, default="Unknown", server_default="Unknown"
    ),
    Column("nickname", String(100), nullable=False),
    Column("power_class", ENUM("S", "A", "B", "C", name="power_class"), nullable=False),
    Column("location", JSON, nullable=False),
    CheckConstraint("length(name) >= 1 AND length(name) <= 100", name="name_length"),
    CheckConstraint(
        "length(nickname) >= 1 AND length(nickname) <= 100", name="nickname_length"
    ),
    UniqueConstraint("name", "nickname", name="name_nickname"),
)
