from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.api.database import create_tables

def create_application() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        create_tables()

    app.include_router(v1_router, prefix="/v1")
    return app

app = create_application()
