import praw


def get_featured_ideologies(comment):
    def extract(segment):
        if "ism" in segment:
            return segment
        if "acy" in segment:
            return segment

    set(comment.split())
