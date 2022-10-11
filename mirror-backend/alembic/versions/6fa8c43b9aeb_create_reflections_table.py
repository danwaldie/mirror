"""create reflections table

Revision ID: 6fa8c43b9aeb
Revises: eabf7ebeb485
Create Date: 2022-10-09 16:26:39.288509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fa8c43b9aeb'
down_revision = 'eabf7ebeb485'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reflections",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("prompt_id", sa.Integer, sa.ForeignKey("prompts.id"), nullable=False, index=True),
        sa.Column("reflection_text", sa.String),
        sa.Column("date_submitted", sa.DateTime(timezone=True))
    )


def downgrade() -> None:
    op.drop_table("reflections")
