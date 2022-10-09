"""add email to users

Revision ID: eabf7ebeb485
Revises: deb277484bf3
Create Date: 2022-10-07 10:40:10.830287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eabf7ebeb485'
down_revision = 'deb277484bf3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("email", sa.String, unique=True, index=True)
    )
    op.create_index(
        "ix_users_username",
        "users",
        ["username"]
    )


def downgrade() -> None:
    op.drop_column(
        "users",
        "email"
    )
