from .ideology import *
import src.data.database.database as Database

Database.create_tables(Base, Database.engine)
