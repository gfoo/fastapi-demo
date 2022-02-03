from core.security import create_access_token, verify_password
from db import users as DBUsers
from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from .deps import get_db

router = APIRouter(
    tags=['authentication']
)


@router.post('/token')
def get_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = DBUsers.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_NOT_FOUND, detail="Inactive user")

    access_token = create_access_token(user_id=user.id)
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
