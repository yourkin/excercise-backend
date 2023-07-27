from fastapi import FastAPI


def create_application() -> FastAPI:
    app = FastAPI()
    return app


app = create_application()