
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import authentication, project, user
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(user.router)
app.include_router(project.router)
app.include_router(authentication.router)
