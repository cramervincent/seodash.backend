from fastapi import FastAPI
from routers import backlinks, auth
from dependencies.dependencies import *
from models import models



app = FastAPI()

origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


# Routes:
app.include_router(backlinks.router, tags=['Backlinks'])
app.include_router(auth.router, tags=['Auth'])

