from datetime import date, datetime
from typing import Optional
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from database import reflections, database



class ReflectionIn(BaseModel):
    user_id: int
    prompt_id: int
    reflection_text: str
    date_submitted: datetime


class Reflection(BaseModel):
    id: int
    user_id: int
    prompt_id: int
    reflection_text: str
    date_submitted: datetime


router = APIRouter()


@router.get("/reflections/", response_model=List[Reflection])
async def read_reflections():
    query = reflections.select()
    return await database.fetch_all(query)


@router.get("/reflections/{prompt_id}/{user_id}/", response_model=Reflection)
async def read_reflection_by_prompt_and_user(prompt_id: int, user_id: int):
    query = reflections.select().where(reflections.c.user_id == user_id, reflections.c.prompt_id == prompt_id)
    return await database.fetch_one(query)


@router.post("/reflections/", response_model=Reflection)
async def create_reflection(reflection: ReflectionIn):
    print(reflection)
    query = reflections.insert().values(
        user_id=reflection.user_id, 
        prompt_id=reflection.prompt_id, 
        reflection_text=reflection.reflection_text, 
        date_submitted=reflection.date_submitted
    )
    last_record_id = await database.execute(query)
    return {**reflection.dict(), "id": last_record_id}