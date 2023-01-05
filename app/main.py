import os
from app import auth, crud, models, schemas
# import crud
# import auth
# import models
# import schemas
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

if not os.path.exists("./sqlitedb"):
    os.makedirs("./sqlitedb")

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()

# origins = ['http://localhost:8000', 'http://127.0.0.1:8000','https://siebevr.github.io/, https://main-service-siebevr.cloud.okteto.net/']
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    # allow_methods=["PUT", "GET", "POST", "DELETE"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# class Rider(BaseModel):
#     id: int
#     naam: str
#     leeftijd: int
#     land: str
#     ploeg: str
#     punten: int

# riders = []

# riders.append(Rider(id=1, naam="Tadej Pogačar", leeftijd=24, land="Slovenië", ploeg="UAE Team Emirates", punten=4839))
# riders.append(Rider(id=2, naam="Wout van Aert", leeftijd=28, land="België", ploeg="Jumbo-Visma", punten=3722))
# riders.append(Rider(id=3, naam="Remco Evenepoel", leeftijd=22, land="België", ploeg="Soudal-Quickstep", punten=3602))
# riders.append(Rider(id=4, naam="Jonas Vingegaard", leeftijd=25, land="Denemarken", ploeg="Jumbo-Visma", punten=3317))
# riders.append(Rider(id=5, naam="Aleksandr Vlasov", leeftijd=26, land="Rusland", ploeg="BORA-Hansgrohe", punten=2105))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/adduser/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/leaderboard", response_model=list[schemas.Rider])
async def sort_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    riders = crud.get_riders(db, skip=skip, limit=limit)
    riders.sort(key=lambda x: x.punten, reverse=True)
    return riders

@app.get("/riders", response_model=list[schemas.Rider])
async def get_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    riders = crud.get_riders(db, skip=skip, limit=limit)
    return riders

@app.get("/rider/{id}", response_model=schemas.Rider)
async def get_rider(id: int, db: Session = Depends(get_db)):
    db_rider = crud.get_rider_by_id(db, id=id)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider

@app.post("/addrider/", response_model=schemas.Rider)
async def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_rider(db, rider)

@app.put("/updaterider/{id}", response_model=schemas.RiderUpdate)
async def update_rider(id: int, rider: schemas.RiderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.update_rider(db=db, id=id, rider=rider)

@app.delete("/deleterider/{id}", response_model=schemas.RiderDelete)
async def delete_rider(id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.delete_rider(db=db, id=id)

@app.get("/ploegen", response_model=list[schemas.Ploeg])
async def get_ploegen(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ploegen = crud.get_ploegen(db, skip=skip, limit=limit)
    return ploegen

@app.post("/addploeg/", response_model=schemas.Ploeg)
async def create_ploeg(ploeg: schemas.PloegCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_ploeg(db, ploeg)




























# @app.get("/")
# async def root():
#     return {"This is the home page"}

# @app.get("/leaderboard")
# async def sort_riders(token: str = Depends(oauth2_scheme)):
#     riders.sort(key=lambda x: x.punten, reverse=True)
#     return riders

# @app.get("/riders")
# async def get_riders():
#     return riders

# @app.get("/rider/{id}")
# async def get_rider(id: int):
#     for i in riders:
#         if i.id == id:
#             return i

# @app.get("/rider/{naam}")
# async def get_rider(naam: str):
#     for i in riders:
#         if i.naam == naam:
#             return i

# @app.post("/addrider/")
# async def add_rider(riderid: int, ridernaam: str, riderleeftijd: int, riderland: str, riderploeg: str, riderpunten: int):
#     for rider in riders:
#         if rider.id == riderid or rider.naam == ridernaam:
#             return "Rider already exists"
#     riders.append(Rider(id=riderid, naam=ridernaam, leeftijd=riderleeftijd, land=riderland, ploeg=riderploeg, punten=riderpunten))
#     return  riders

# @app.delete("/deleterider/")
# async def delete_rider(riderid: int):
#     for i in riders:
#         if i.id == riderid:
#             riders.remove(i)
#     return riders

# @app.put("/updaterider/")
# async def update_rider(riderid: int, ridernaam: str, riderleeftijd: int, riderland: str, riderploeg: str, riderpunten: int):
#     for i in riders:
#         if i.id == riderid:
#             i.leeftijd = riderleeftijd
#             i.land = riderland
#             i.ploeg = riderploeg
#             i.punten = riderpunten
#     return riders
