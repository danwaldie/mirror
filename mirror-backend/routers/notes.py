from typing import Optional
from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from database import notes, database



class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


router = APIRouter()


@router.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@router.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    print(note)
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}