

from pydantic import BaseModel


class User(BaseModel):
    email: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserView(User):
    id: int


class UserCreate(User):
    password: str
