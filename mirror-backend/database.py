import os
import databases
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

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

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
