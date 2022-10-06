"""create prompts table

Revision ID: deb277484bf3
Revises: 4e436ea36437
Create Date: 2022-10-06 11:42:47.882698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deb277484bf3'
down_revision = '4e436ea36437'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "prompts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("prompt_text", sa.String),
        sa.Column("date_published", sa.Date)
    )


def downgrade() -> None:
    op.drop_table("prompts")
