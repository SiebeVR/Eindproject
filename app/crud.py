import crud
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import models
import schemas
import auth

SECRET_KEY = "0a426850ff6a6fe27fb27bdbe1977790052cf6ef2494c1c765ab69aad6851953"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes of expiration time if ACCESS_TOKEN_EXPIRE_MINUTES variable is empty
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Adding the JWT expiration time case
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_rider_by_id(db: Session, id: int):
    return db.query(models.Rider).filter(models.Rider.id == id).first()

def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def get_rider_by_name(db: Session, naam: str):
    return db.query(models.Rider).filter(models.Rider.naam == naam).first()

def get_leaderboard(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def create_rider(db: Session, rider: schemas.RiderCreate):
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
    db_user = models.User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

