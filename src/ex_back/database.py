import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ex_back.config import get_settings

log = logging.getLogger("uvicorn")

DATABASE_URL = get_settings().sync_database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    log.info("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    log.info("Database and tables created.")
