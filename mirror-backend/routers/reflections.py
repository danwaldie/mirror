from . import users
from . import prompts
from typing import List
from fastapi import Depends, APIRouter, HTTPException
from ..database import reflections, database
from ..models.models import Reflection, ReflectionIn


router = APIRouter(
    tags=["Reflections"]
)

async def get_reflection_prompt_user(prompt_id: int, user_id: int):
    query = reflections.select().where(reflections.c.user_id == user_id, reflections.c.prompt_id == prompt_id)
    return await database.fetch_one(query)


async def get_reflection_id(id: int):
    query = reflections.select().where(reflections.c.id == id)
    return await database.fetch_one(query)


async def get_current_user_today_reflection(
    current_user: users.User = Depends(users.get_current_user), 
    current_prompt: prompts.Prompt = Depends(prompts.get_todays_prompt)
    ):
    query = reflections.select().where(reflections.c.user_id == current_user.id, reflections.c.prompt_id == current_prompt.id)
    reflection = await database.fetch_one(query)
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")
    return reflection


@router.get("/reflections/", response_model=List[Reflection])
async def read_reflections():
    query = reflections.select()
    return await database.fetch_all(query)


@router.get("/reflections/today/me/", response_model=Reflection)
async def read_today_reflection_by_current_user(todays_reflection: Reflection = Depends(get_current_user_today_reflection)):
    return todays_reflection


@router.get("/reflections/{prompt_id}/{user_id}/", response_model=Reflection)
async def read_reflection_by_prompt_and_user(reflection: Reflection = Depends(get_reflection_prompt_user)):
    return reflection


@router.get("/reflections/{id}/", response_model=Reflection)
async def read_reflection_by_id(reflection: Reflection = Depends(get_reflection_id)):
    return reflection


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