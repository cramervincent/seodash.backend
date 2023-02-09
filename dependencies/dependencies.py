from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from dependencies.database import SessionLocal, engine
from contextvars import ContextVar

def get_db():
    try:
        db = SessionLocal()
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar('db_session')
