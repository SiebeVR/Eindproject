from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True

class UserBase(MyBaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # is_active: bool
    

class Rider(MyBaseModel):
    id: int
    naam: str
    leeftijd: int
    land: str
    ploeg: str
    punten: int

class RiderCreate(Rider):
    pass

class RiderUpdate(Rider):
    pass

class RiderDelete(Rider):
    pass
