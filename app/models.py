from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base




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
    punten = Column(Integer)
    ploeg = Column(String, ForeignKey("ploegen.naam"))

    Link = relationship("Ploeg", back_populates="Links")
    
    
class Ploeg(Base):
    __tablename__ = "ploegen"

    naam = Column(String, primary_key=True, index=True)
    land = Column(String)

    Links = relationship("Rider", back_populates="Link")
