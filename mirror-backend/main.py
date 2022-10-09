from database import database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, notes, prompts, reflections


app = FastAPI()
app.include_router(users.router)
app.include_router(notes.router)
app.include_router(prompts.router)
app.include_router(reflections.router)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

