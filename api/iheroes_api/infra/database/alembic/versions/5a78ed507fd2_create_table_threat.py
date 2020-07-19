"""Create table threat.

Revision ID: 5a78ed507fd2
Revises: 394a7cf4bd00
Create Date: 2020-07-19 22:50:33.254129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5a78ed507fd2"
down_revision = "394a7cf4bd00"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "threat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column(
            "danger_level",
            postgresql.ENUM("wolf", "tiger", "dragon", "god", name="danger_level"),
            nullable=False,
        ),
        sa.Column("location", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_threat")),
        sa.UniqueConstraint("name", name=op.f("uq_threat_name")),
    )


def downgrade():
    op.drop_table("threat")
    sa.Enum(name="danger_level").drop(op.get_bind(), checkfirst=False)
