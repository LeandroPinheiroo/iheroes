"""Change hero constraint name.

Revision ID: 394a7cf4bd00
Revises: 6be2fd1cda19
Create Date: 2020-07-19 22:48:14.752886

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "394a7cf4bd00"
down_revision = "6be2fd1cda19"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("name_nickname", "hero", ["name", "nickname"])
    op.drop_constraint("uq_hero_name_nickname", "hero", type_="unique")


def downgrade():
    op.create_unique_constraint("uq_hero_name_nickname", "hero", ["name", "nickname"])
    op.drop_constraint("name_nickname", "hero", type_="unique")
