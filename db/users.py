
from core.security import get_password_hash
from models.user import DBUser
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBUser).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = DBUser(
        email=user.email,
        fullname=user.fullname,
        password=get_password_hash(user.password),
        is_active=user.is_active,
        is_superuser=user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db.query(DBUser).filter(
        DBUser.id == user_id).delete()
    db.commit()


def update_user_password(db: Session, user_id: int, new_password: str):
    db.query(DBUser).filter(
        DBUser.id == user_id).update({
            DBUser.password: get_password_hash(new_password)
        })
    db.commit()


def update_user_activate(db: Session, user_id: int, activate: bool):
    db.query(DBUser).filter(
        DBUser.id == user_id).update({
            DBUser.is_active: activate
        })
    db.commit()


def update_user_superuser(db: Session, user_id: int, superuser: bool):
    db.query(DBUser).filter(
        DBUser.id == user_id).update({
            DBUser.is_superuser: superuser
        })
    db.commit()
