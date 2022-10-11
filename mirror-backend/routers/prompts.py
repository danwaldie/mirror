from datetime import date, datetime
from time import strptime
from typing import List
from fastapi import Depends, APIRouter
from database import prompts, database
from models.models import Prompt, PromptIn


router = APIRouter(
    tags=["Prompts"]
)


async def get_todays_prompt():
    query = prompts.select().where(prompts.c.date_published == date.today())
    return await database.fetch_one(query)


@router.get("/prompts/today/", response_model=Prompt)
async def read_todays_prompt(prompt: Prompt = Depends(get_todays_prompt)):
    return prompt

@router.get("/prompts/{date_string}/", response_model=Prompt)
async def read_prompt_by_date(date_string: str):
    search_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    query = prompts.select().where(prompts.c.date_published == search_date)
    return await database.fetch_one(query)

@router.get("/prompts/{prompt_id}/", response_model=Prompt)
async def read_prompt(prompt_id: int):
    query = prompts.select().where(prompts.c.id == prompt_id)
    return await database.fetch_one(query)

@router.get("/prompts/", response_model=List[Prompt])
async def read_prompts():
    query = prompts.select()
    return await database.fetch_all(query)

@router.post("/prompts/", response_model=Prompt)
async def create_prompt(prompt: PromptIn):
    print(prompt)
    query = prompts.insert().values(prompt_text=prompt.prompt_text, date_published=prompt.date_published)
    last_record_id = await database.execute(query)
    return {**prompt.dict(), "id": last_record_id}