from fastapi import FastAPI
from routers import backlinks
from dependencies.dependencies import *
from models import models
from dependencies.database import SessionLocal, engine

app = FastAPI(ssl_keyfile="/path/to/your/private.key", ssl_certfile="files/api.seodash.vincent-dev.xyz.crt")

origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(backlinks.router, tags=['backlinks'])

