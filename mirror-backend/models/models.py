from datetime import date, datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ReflectionIn(BaseModel):
    user_id: int
    prompt_id: int
    reflection_text: str
    date_submitted: datetime
    mood: str


class Reflection(BaseModel):
    id: int
    user_id: int
    prompt_id: int
    reflection_text: str
    date_submitted: datetime
    mood: str | None


class UserBase(BaseModel):
    username: str | None = None
    email: str
    disabled: bool | None


class User(UserBase):
    id: int | None
    reflections: list[Reflection] | None = []

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    hashed_password: str


class UserIn(UserBase):
    password: str


class PromptIn(BaseModel):
    prompt_text: str
    date_published: date | None = None


class Prompt(BaseModel):
    id: int
    prompt_text: str
    date_published: date | None = None

    class Config:
        orm_mode = True
