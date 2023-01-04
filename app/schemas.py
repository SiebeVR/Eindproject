from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class RiderBase(BaseModel):
    naam: str
    leeftijd: int
    land: str
    ploeg: str
    punten: int

class RiderCreate(RiderBase):
    pass

class RiderUpdate(RiderBase):
    pass

class PloegBase(BaseModel):
    naam: str
    land: str

class PloegCreate(PloegBase):
    pass

class PloegUpdate(PloegBase):
    pass
