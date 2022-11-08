import os
import databases
import sqlalchemy
from .config import settings

DATABASE_URL = settings.database_url

database = databases.Database(DATABASE_URL + '?min_size=5&max_size=15')

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, index=True, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, index=True, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String)
)

prompts = sqlalchemy.Table(
    "prompts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("prompt_text", sqlalchemy.String),
    sqlalchemy.Column("date_published", sqlalchemy.Date)
)

reflections = sqlalchemy.Table(
    "reflections",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False, index=True),
    sqlalchemy.Column("prompt_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("prompts.id"), nullable=False, index=True),
    sqlalchemy.Column("reflection_text", sqlalchemy.String),
    sqlalchemy.Column("date_submitted", sqlalchemy.DateTime(timezone=True)),
    sqlalchemy.Column("mood", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
