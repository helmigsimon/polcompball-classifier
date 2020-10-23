from .base import Base
from .database import engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import OperationalError


class Ideology(Base):
    __tablename__ = "ideologies"
    __fields__ = (
        "id",
        "name",
        "page_url",
        "thumbnail_url",
        "position",
        "canon",
        "non_canon",
        "party",
        "movement",
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    page_url = Column(String)
    thumbnail_url = Column(String)
    position = Column(String)
    canon = Column(Boolean)
    non_canon = Column(Boolean)
    party = Column(Boolean)
    movement = Column(Boolean)

    def __init__(self, *args, **kwargs):
        super(Ideology, self).__init__(*args, **kwargs)


try:
    # Creates tables
    Base.metadata.create_all(bind=engine)
except OperationalError:
    pass
except Exception:
    raise