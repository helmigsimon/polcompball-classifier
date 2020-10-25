import os
from peewee import *
from dotenv import load_dotenv, find_dotenv
from playhouse.sqlite_ext import SqliteExtDatabase

load_dotenv(find_dotenv())

polcompball_db = os.environ.get("POLCOMPBALL_DB")
database = SqliteExtDatabase(polcompball_db)


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class Ideology(BaseModel):
    class Meta:
        table_name = "ideology"

    canon = BooleanField(null=True)
    movement = BooleanField(null=True)
    name = CharField(null=True, unique=True)
    non_canon = BooleanField(null=True)
    page_url = CharField(null=True)
    party = BooleanField(null=True)
    position = CharField(null=True)
    thumbnail_url = CharField(null=True)

    @database.connection_context()
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @classmethod
    @database.connection_context()
    def create(cls, *args, **kwargs):
        return super().create(*args, **kwargs)

    @classmethod
    @database.connection_context()
    def delete(cls, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @database.connection_context()
    def delete_instance(self, *args, **kwargs):
        return super().delete_instance(*args, **kwargs)

    @classmethod
    @database.connection_context()
    def select(cls, *args, **kwargs):
        return super().select(*args, **kwargs)


class Submission(BaseModel):
    class Meta:
        table_name = "submission"

    submission_id = CharField(null=False, unique=True)
    created_utc = DateTimeField(null=False)
    is_original_content = BooleanField(null=False)
    score = FloatField(null=False)
    title = CharField(null=False)
    upvote_ratio = FloatField(null=False)
    url = CharField(null=False)


class Comment(BaseModel):
    class Meta:
        table_name = "comment"

    submission = ForeignKeyField(Submission, backref="comments")
    author = CharField(null=False)
    is_submitter = BooleanField(null=False)
    created_utc = DateTimeField(null=False)
    body = CharField(null=False)
    permalink = CharField(null=False)
    score = FloatField(null=False)


if __name__ == "__main__":
    database.connect()
    database.create_tables([Ideology, Submission, Comment])
