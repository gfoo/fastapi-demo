

from pydantic import BaseModel


class UserBase(BaseModel):
    fullname: str

    class Config:
        orm_mode = True


class User(UserBase):
    email: str
    is_active: bool
    is_superuser: bool


class UserView(User):
    id: int


class UserProject(UserBase):
    id: int


class UserCreate(User):
    password: str


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str


class UserUpdateActivate(BaseModel):
    activate: bool


class UserUpdateSuperuser(BaseModel):
    superuser: bool
