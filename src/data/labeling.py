import re
import src.data.database as db
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Remove text in parentheses and strip whitespace
re_paren_text = re.compile(r"\s+\([^)]*\)")
re_symbols = re.compile(r"[\W_]+")
re_url = re.compile(r"http\S+")


normalize_label = lambda x: re_paren_text.sub(unidecode(x), "")

LABELS = [
    normalize_label(ideology.__data__["name"]) for ideology in db.Ideology.select()
]
LABEL_URL_HASH = {
    ideology.__data__["page_url"]: ideology.__data__["id"]
    for ideology in db.Ideology.select()
}
STOPWORDS_EN = set(stopwords.words("english"))


def clean_comment_1(comment):
    """
    Try and filter out the ideologies for each
    """
    comment = re_url.sub("", comment)

    comment = re_symbols.sub(" ", comment)

    comment = [w for w in word_tokenize(comment) if w not in STOPWORDS_EN]

    return comment


def clean_comment_2(comment):
    """
    Parse out the urls and take the ideology from there
    """
    comment = re_url.findall(comment)

    labels = [LABEL_URL_HASH.get(url.strip(")"), None) for url in comment]

    labels = [str(label) for label in labels if label is not None]

    if len(labels) == 0:
        return None
    return ", ".join(labels)
