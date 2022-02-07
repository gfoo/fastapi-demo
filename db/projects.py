

from core.security import get_password_hash
from models.project import DBProject
from models.user import DBUser
from schemas.project import Project
from sqlalchemy import or_
from sqlalchemy.orm import Session


def create_project(db: Session, project: Project, owner_id: int):
    db_project = DBProject(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBProject).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(DBProject).filter(DBProject.id == project_id).first()


def get_project_by_name(db: Session, name: str):
    return db.query(DBProject).filter(DBProject.name == name).first()


def get_projects_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return (db.query(DBProject)
            .filter(or_(DBProject.owner_id == owner_id, DBProject.private == False))
            .offset(skip)
            .limit(limit)
            .all()
            )


def delete_project(db: Session, project_id: int):
    db.query(DBProject).filter(
        DBProject.id == project_id).delete()
    db.commit()


def update_project(db: Session, project_id: int,
                   name: str, description: str, private: bool):
    db.query(DBProject).filter(
        DBProject.id == project_id).update({
            DBProject.name: name,
            DBProject.description: description,
            DBProject.private: private
        })
    db.commit()
