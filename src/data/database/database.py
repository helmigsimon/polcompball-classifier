from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import OperationalError
import os

load_dotenv(find_dotenv())

polcompball_db = os.environ.get("POLCOMPBALL_DB")
engine = create_engine(polcompball_db)


def create_tables(Base, engine):
    try:
        # Creates tables
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        pass
    except Exception:
        raise


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def perform_operation(operation, objects):
    with session_scope() as session:
        return getattr(session, operation)(objects)


def insert(objects):
    if isinstance(objects, list) or isinstance(objects, tuple):
        perform_operation("add_all", objects)
    else:
        perform_operation("add", objects)


def delete(objects):
    if isinstance(objects, list) or isinstance(objects, tuple):
        for obj in objects:
            perform_operation("delete", obj)
    else:
        perform_operation("delete", objects)


def query(model):
    return perform_operation("query", model)
