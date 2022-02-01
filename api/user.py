from typing import List

from db import users as DBUsers
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import DBUser
from schemas.user import UserCreate, UserView
from sqlalchemy.orm import Session

from .deps import get_current_active_superuser, get_current_active_user, get_db

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=List[UserView])
def get_all_users(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db),
                  current_user: DBUser = Depends(get_current_active_superuser)):
    """
    Retrieve users.
    """
    return DBUsers.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserView)
def get_user(user_id: int, db: Session = Depends(get_db),
             current_user: DBUser = Depends(get_current_active_user)):
    """
    Retrieve a user (only itself if not enough privileges).
    """
    db_user = DBUsers.get_user(db, user_id=user_id)
    if db_user == current_user:
        return db_user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user does not have enough privileges"
        )
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user


@router.post("/", response_model=UserView)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                current_user: DBUser = Depends(get_current_active_superuser)):
    """
    Create a user.
    """
    db_user = DBUsers.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return DBUsers.create_user(db=db, user=user)
