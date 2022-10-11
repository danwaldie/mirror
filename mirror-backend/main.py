from database import database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, notes, prompts, reflections
import sentry_sdk


sentry_sdk.init(
    dsn="https://198f74af49e648ad90dfcbae23d8ef24@o4503964181528576.ingest.sentry.io/4503964183035905",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


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


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
