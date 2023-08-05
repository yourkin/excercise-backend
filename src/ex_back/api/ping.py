from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    # The purpose of this endpoint is to provide a minimal health check for the backend.
    return {
        "ping": "pong!",
    }
