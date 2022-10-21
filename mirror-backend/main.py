from .database import database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, prompts, reflections
from .config import settings
import sentry_sdk


sentry_sdk.init(
    dsn=settings.sentry_dsn,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


app = FastAPI()
app.include_router(users.router)
app.include_router(prompts.router)
app.include_router(reflections.router)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://mirror-frontend-it68kvtss-danwaldie.vercel.app",
    "https://vercel.com/danwaldie/mirror-frontend",
    "https://mirror-opal-six.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origin_regex='.*',
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
