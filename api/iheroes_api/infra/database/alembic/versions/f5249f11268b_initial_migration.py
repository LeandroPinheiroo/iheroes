"""Initial migration.

Revision ID: f5249f11268b
Revises:
Create Date: 2020-06-09 04:15:15.999815

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f5249f11268b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("email", name=op.f("uq_user_email")),
    )


def downgrade():
    op.drop_table("user")
