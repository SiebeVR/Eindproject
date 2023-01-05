from sqlalchemy.orm import Session
import models
import schemas
import auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



def get_rider_by_id(db: Session, id: int):
    return db.query(models.Rider).filter(models.Rider.id == id).first()

def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def get_rider_by_name(db: Session, naam: str):
    return db.query(models.Rider).filter(models.Rider.naam == naam).first()

def get_leaderboard(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def create_rider(db: Session, rider: schemas.Rider):
    db_rider = models.Rider(id=rider.id, naam=rider.naam, leeftijd=rider.leeftijd, land=rider.land, ploeg=rider.ploeg, punten=rider.punten)
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

def delete_rider(db: Session, id: int):
    db_rider = db.query(models.Rider).filter(models.Rider.id == id).first()
    db.delete(db_rider)
    db.commit()
    return db_rider

def update_rider(db: Session, id: int, rider: schemas.RiderCreate):
    db_rider = db.query(models.Rider).filter(models.Rider.id == id).first()
    db_rider.naam = rider.naam
    db_rider.leeftijd = rider.leeftijd
    db_rider.land = rider.land
    db_rider.ploeg = rider.ploeg
    db_rider.punten = rider.punten
    db.commit()
    return db_rider

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_ploegen(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ploeg).offset(skip).limit(limit).all()

def create_ploeg(db: Session, ploeg: schemas.Ploeg):
    db_ploeg = models.Ploeg(naam=ploeg.naam, land=ploeg.land)
    db.add(db_ploeg)
    db.commit()
    db.refresh(db_ploeg)
    return db_ploeg
