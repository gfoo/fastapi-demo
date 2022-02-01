
from fastapi import FastAPI

from api import authentication, user
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user.router)
app.include_router(authentication.router)
