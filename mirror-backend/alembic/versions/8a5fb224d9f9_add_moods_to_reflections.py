"""add moods to reflections

Revision ID: 8a5fb224d9f9
Revises: 6fa8c43b9aeb
Create Date: 2022-10-24 15:55:53.078122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5fb224d9f9'
down_revision = '6fa8c43b9aeb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "reflections",
        sa.Column("mood", sa.String)
    )


def downgrade() -> None:
    op.drop_column(
        "reflections",
        "mood"
    )
