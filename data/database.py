import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import BASE_DIR

DATABASE_FILE_PATH = os.path.join(BASE_DIR, "database.db")

Base = declarative_base()

engine = create_engine(f"sqlite:///{DATABASE_FILE_PATH}")
Session = sessionmaker(bind=engine)

def create_tables_if_not_exists():
    Base.metadata.create_all(bind=engine)

@contextmanager
def read_only_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def read_write_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
