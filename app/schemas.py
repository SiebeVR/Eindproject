from pydantic import BaseModel

class PloegBase(BaseModel):
    title: str
    description: str | None = None


class PloegCreate(PloegBase):
    pass


class Ploeg(PloegBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class RiderBase(BaseModel):
    naam: str
    leeftijd: int
    land: str
    ploeg: str
    punten: int


class RiderCreate(RiderBase):
    pass


class Rider(RiderBase):
    id: int

    class Config:
        orm_mode = True