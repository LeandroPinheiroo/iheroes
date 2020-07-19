"""Create table threat_record.

Revision ID: 100e40af3a2d
Revises: 5a78ed507fd2
Create Date: 2020-07-19 23:05:48.498953

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from iheroes_api.infra.database.sqlalchemy import metadata

# revision identifiers, used by Alembic.
revision = "100e40af3a2d"
down_revision = "5a78ed507fd2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "threat_record",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("threat_id", sa.Integer(), nullable=False),
        sa.Column(
            "danger_level",
            postgresql.ENUM(
                "wolf", "tiger", "dragon", "god", name="danger_level", metadata=metadata
            ),
            nullable=False,
        ),
        sa.Column("location", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["threat_id"], ["threat.id"], name=op.f("fk_threat_record_threat_id_threat")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_threat_record")),
    )


def downgrade():
    op.drop_table("threat_record")
