from app.auth import verify_password, get_password_hash
from sqlalchemy.orm import Session
from models import Rider, User, Ploeg
from schemas import RiderCreate, RiderUpdate, UserCreate, UserUpdate, PloegBase, PloegCreate, PloegUpdate


def get_rider_by_id(db: Session, id: int):
    return db.query(Rider).filter(Rider.id == id).first()

def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rider).offset(skip).limit(limit).all()

def get_rider_by_name(db: Session, naam: str):
    return db.query(Rider).filter(Rider.naam == naam).first()

def get_leaderboard(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rider).offset(skip).limit(limit).all()

def create_rider(db: Session, rider: RiderCreate):
    db_rider = Rider(id=rider.id, naam=rider.naam, leeftijd=rider.leeftijd, land=rider.land, ploeg=rider.ploeg, punten=rider.punten)
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

def delete_rider(db: Session, id: int):
    db_rider = db.query(Rider).filter(Rider.id == id).first()
    db.delete(db_rider)
    db.commit()
    return db_rider

def update_rider(db: Session, id: int, rider: RiderCreate):
    db_rider = db.query(Rider).filter(Rider.id == id).first()
    db_rider.naam = rider.naam
    db_rider.leeftijd = rider.leeftijd
    db_rider.land = rider.land
    db_rider.ploeg = rider.ploeg
    db_rider.punten = rider.punten
    db.commit()
    return db_rider


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
