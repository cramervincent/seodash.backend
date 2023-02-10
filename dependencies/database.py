from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
PRODUCTION_DB = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PSW')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PSW')}@{os.getenv('DB_PORT')}/{os.getenv('DB_PSW')}@{os.getenv('DB_DEF_DATABASE')}"
DEVELOPMENT_DB = "sqlite:///./db/database.db"

# os.getenv('JWT_SECRET')
if os.getenv('ENVIROMENT') == 'production':
    sql_db_url = PRODUCTION_DB
else:
    sql_db_url = DEVELOPMENT_DB

SQLALCHEMY_DATABASE_URL = sql_db_url
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

if os.getenv('ENVIROMENT') == 'production':
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
        )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 