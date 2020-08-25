"""Create table occurrences.

Revision ID: ecf3ad3a019a
Revises: 100e40af3a2d
Create Date: 2020-08-25 22:22:03.209075

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ecf3ad3a019a"
down_revision = "100e40af3a2d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "occurrence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("threat_id", sa.Integer(), nullable=False),
        sa.Column(
            "state",
            postgresql.ENUM(
                "pending", "active", "resolved", name="occurrence_state", nullable=False
            ),
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["threat_id"], ["threat.id"], name=op.f("fk_occurrence_threat_id_threat")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_occurrence")),
    )


def downgrade():
    op.drop_table("occurrence")
    sa.Enum(name="occurrence_state").drop(op.get_bind(), checkfirst=False)
