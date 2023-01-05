from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    # email = Column(String, unique=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
    

class Rider(Base):
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String)
    leeftijd = Column(Integer)
    land = Column(String)
    ploeg = Column(String)
    punten = Column(Integer)
    
class Ploeg(Base):
    __tablename__ = "ploegen"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String, unique=True)
    land = Column(String)
    # Rider = relationship("Rider", back_populates="Ploeg")