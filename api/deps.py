from core.config import settings
from core.security import JWT_ALGORITHM
from db import users as DBUsers
from db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from models.user import DBUser
from pydantic import ValidationError
from schemas.token import TokenPayload
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> DBUser:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = DBUsers.get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(
    current_user: DBUser = Depends(get_current_user),
) -> DBUser:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: DBUser = Depends(get_current_active_user),
) -> DBUser:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user does not have enough privileges"
        )
    return current_user
