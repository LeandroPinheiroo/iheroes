from sqlalchemy.dialects.postgresql import ENUM

from iheroes_api.infra.database.sqlalchemy import metadata

DangerLevelEnum = ENUM(
    "wolf", "tiger", "dragon", "god", name="danger_level", metadata=metadata
)
