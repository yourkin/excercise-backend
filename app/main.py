from fastapi import FastAPI

from app.api.v1.router import router as v1_router

def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(v1_router, prefix="/v1")
    return app


app = create_application()