import os
import auth
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

if not os.path.exists("./sqlitedb/sql_app.db"):
    os.makedirs("./sqlitedb/sql_app.db")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

   
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
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/leaderboard", response_model=List[schemas.Rider])
async def sort_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    riders = crud.get_riders(db, skip=skip, limit=limit)
    riders.sort(key=lambda x: x.punten, reverse=True)
    return riders

@app.get("/riders", response_model=List[schemas.Rider])
async def get_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    riders = crud.get_riders(db, skip=skip, limit=limit)
    return riders

@app.get("/rider/{id}", response_model=schemas.Rider)
async def get_rider(id: int, db: Session = Depends(get_db)):
    db_rider = crud.get_rider(db, id=id)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider

@app.get("/rider/{naam}", response_model=schemas.Rider)
async def get_rider(naam: str, db: Session = Depends(get_db)):
    db_rider = crud.get_rider(db, naam=naam)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_rider

@app.post("/rider", response_model=schemas.Rider)
async def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.create_rider(db=db, rider=rider)

@app.put("/rider/{id}", response_model=schemas.Rider)
async def update_rider(id: int, rider: schemas.RiderCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.update_rider(db=db, id=id, rider=rider)

@app.delete("/rider/{id}", response_model=schemas.Rider)
async def delete_rider(id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.delete_rider(db=db, id=id)

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
