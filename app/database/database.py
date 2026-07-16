import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fasalseva.db")


def _create_engine() -> object:
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    try:
        return create_engine(DATABASE_URL, pool_pre_ping=True)
    except Exception:
        fallback_url = "sqlite:///./fasalseva.db"
        return create_engine(fallback_url, connect_args={"check_same_thread": False})


engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import user, farmer, storage_owner, storage, booking, prediction_history, weather_log, scheme

    global engine

    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        fallback_url = "sqlite:///./fasalseva.db"
        engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
        SessionLocal.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
