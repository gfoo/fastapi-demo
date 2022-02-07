

from pydantic import BaseModel

from schemas.user import UserProject


class Project(BaseModel):
    name: str
    description: str
    private: bool

    class Config:
        orm_mode = True


class ProjectView(Project):
    id: int
    owner: UserProject
