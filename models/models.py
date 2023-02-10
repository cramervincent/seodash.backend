from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dependencies.database import Base


class Backlinks(Base):
    __tablename__ = "backlinks"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)
    site = Column(String, index=True)
    status = Column(String, index=True)
    pa = Column(String, index=True)
    da = Column(String, index=True)
    last_check = Column(String, index=True)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)