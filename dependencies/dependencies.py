from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from dependencies.database import SessionLocal, engine
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()