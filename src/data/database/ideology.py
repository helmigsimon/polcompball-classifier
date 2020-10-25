from .base import Base
from sqlalchemy import Column, Integer, String, Boolean


class Ideology(Base):
    """
    Ideology Model for SQL Database
    """

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
