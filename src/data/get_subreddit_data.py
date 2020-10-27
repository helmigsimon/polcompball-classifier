import praw
from tqdm import tqdm
from .database import Submission, Comment


def save_submission(submission):
    submission_instance = Submission(
        submission_id=submission.id,
        **{
            arg: getattr(submission, arg)
            for arg in Submission._meta.columns.keys()
            if arg not in ("id", "submission_id")
        }
    )
    submission_instance.save()
    return submission_instance


def filter_submission(submission):
    # Check if submission is a text post
    try:
        if not isinstance(submission, praw.models.Submission):
            return False
        if submission.is_self:
            return False
        # Check if submission already exists
        if Submission.select().where(Submission.submission_id == submission.id):
            return False
        return True
    except Exception as e:
        print(submission)
        print(submission.__dict__)
        raise


from multiprocessing import Pool


def add_submission_to_database(submission):
    if not filter_submission(submission):
        return
    submission_instance = save_submission(submission)

    for comment in submission.comments:
        if not filter_comment(comment):
            continue

        save_comment(comment, submission_instance)
    return


def filter_comment(comment):
    if isinstance(comment, praw.models.MoreComments):
        return False
    if not comment.is_submitter:
        return False
    return True


def save_comment(comment, submission):
    comment_instance = Comment(
        submission=submission,
        **{
            arg: getattr(comment, arg)
            for arg in Comment._meta.columns.keys()
            if arg not in ("id", "submission_id")
        }
    )
    comment_instance.save()