
from typing import List

from db import projects as DBProjects
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.user import DBUser
from schemas.project import Project, ProjectView
from sqlalchemy.orm import Session

from .deps import get_current_active_user, get_db

router = APIRouter(
    prefix='/projects',
    tags=['projects']
)


@router.get("/", response_model=List[ProjectView])
def get_projects(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: DBUser = Depends(get_current_active_user)):
    """
    Retrieve all projects of current user or all projects if superuser.
    """
    if current_user.is_superuser:
        projects = DBProjects.get_projects(db, skip=skip, limit=limit)
    else:
        projects = DBProjects.get_projects_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return projects


@router.get("/{project_id}", response_model=ProjectView)
def get_project(project_id: int,
                db: Session = Depends(get_db),
                current_user: DBUser = Depends(get_current_active_user)):
    ...
    """
    Retrieve a project (only user's project or public project, superuser can see all projects).
    """
    db_proj = DBProjects.get_project(db, project_id=project_id)
    if db_proj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if (db_proj.owner_id == current_user.id
            or current_user.is_superuser or not db_proj.private):
        return db_proj

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user does not have enough privileges"
    )


def check_existing_project_name(db: Session, name: str, project_id: int = None):
    db_proj = DBProjects.get_project_by_name(db, name=name)
    if db_proj and (db_proj.id != project_id or project_id is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Project name already used")


@router.post("/", response_model=ProjectView)
def create_project(project: Project, db: Session = Depends(get_db),
                   current_user: DBUser = Depends(get_current_active_user)):
    """
    Create a project of current user.
    """
    check_existing_project_name(db, project.name)
    return DBProjects.create_project(db, project, current_user.id)


@router.delete("/{project_id}", response_class=JSONResponse)
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   current_user: DBUser = Depends(get_current_active_user)):
    """
    Delete a project (project's owner or superuser privileges).
    """
    db_proj = DBProjects.get_project(db, project_id=project_id)
    if db_proj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if (db_proj.owner_id == current_user.id
            or current_user.is_superuser):
        DBProjects.delete_project(db=db, project_id=project_id)
        return JSONResponse(content={"status": "ok", "project_id": project_id})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user does not have enough privileges")


@router.post("/{project_id}", response_model=ProjectView)
def update_project(
        project_id: int, project: Project, db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user)):
    """
    Update project (require superuser privileges).
    """
    db_proj = DBProjects.get_project(db, project_id=project_id)
    if db_proj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if (db_proj.owner_id == current_user.id):
        check_existing_project_name(db, project.name, project_id)
        DBProjects.update_project(
            db=db, project_id=project_id,
            name=project.name, description=project.description,
            private=project.private)
        return db_proj

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user does not have enough privileges")
