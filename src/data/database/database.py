from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

load_dotenv(find_dotenv())

polcompball_db = os.environ.get("POLCOMPBALL_DB")
print(polcompball_db)
engine = create_engine(polcompball_db)

Session = sessionmaker()
Session.configure(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_operation(operation, objects):
    with session_scope() as session:
        # print(getattr(session, operation))
        # print(objects)
        getattr(session, operation)(objects)


def db_add(objects):
    if isinstance(objects, list) or isinstance(objects, tuple):
        db_operation("add_all", objects)
    else:
        db_operation("add", objects)


def db_delete(objects):
    if isinstance(objects, list) or isinstance(objects, tuple):
        for obj in objects:
            db_operation("delete", obj)
    else:
        db_operation("delete", objects)
