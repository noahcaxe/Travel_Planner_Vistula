from fastapi import FastAPI
from app.core.middleware.error_handler import error_handler
from app.router.auth import router as auth_router
from app.router.projects import router as projects_router
from app.router.places import router as places_router
from app.core.config.logging_config import setup_logging
from app.core.container import lifespan
setup_logging()
app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(places_router)



@app.middleware("http")
async def global_error_middleware(request, call_next):
    return await error_handler(request, call_next)
