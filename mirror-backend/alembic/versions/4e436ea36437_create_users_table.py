"""create users table

Revision ID: 4e436ea36437
Revises: 3ada648f53d5
Create Date: 2022-10-03 21:58:40.755745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e436ea36437'
down_revision = '3ada648f53d5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True),
        sa.Column("hashed_password", sa.String)
    )


def downgrade():
    op.drop_table("users")
