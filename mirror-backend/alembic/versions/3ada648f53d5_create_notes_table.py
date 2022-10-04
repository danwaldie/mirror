"""create notes table

Revision ID: 3ada648f53d5
Revises: 
Create Date: 2022-10-01 10:57:26.249057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ada648f53d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("text", sa.String),
        sa.Column("completed", sa.Boolean)
    )


def downgrade() -> None:
    op.drop_table("notes")
