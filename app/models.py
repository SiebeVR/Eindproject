from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String)
    leeftijd = Column(Integer)
    land = Column(String)
    ploeg = Column(String)
    punten = Column(Integer)
    