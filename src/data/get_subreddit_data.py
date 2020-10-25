import praw
from .database import database as Database, Submission, Comment


def filter_submission(submission):
    if Database.