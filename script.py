from collections import defaultdict, namedtuple
import os
from operator import attrgetter
from statistics import mean
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from textblob import TextBlob

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])
session = sessionmaker(engine)()

feedback_table = 'bites_biteconsumer'

# https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html
metadata = MetaData()
metadata.reflect(engine, only=[feedback_table])

Base = automap_base(metadata=metadata)
Base.prepare()

SA_TABLE = getattr(Base.classes, feedback_table)
Comment = namedtuple("Comment", "text polarity")


def _get_feedbacks():
    feedbacks = session.query(SA_TABLE.bite_id, SA_TABLE.comments).filter(
        and_(SA_TABLE.comments != None, SA_TABLE.comments != '')  # noqa E711
    )
    return feedbacks


def _get_sentiments_per_bite(feedbacks, bite_id=None):
    if bite_id is not None:
        feedbacks = feedbacks.filter(SA_TABLE.bite_id == bite_id)

    bite_sentiments = defaultdict(list)
    for feedback in feedbacks.all():
        bite_id, comment = feedback
        comment = comment.replace("\r\n", " ")
        sentiment = TextBlob(comment).sentiment
        bite_sentiments[bite_id].append(
            Comment(text=comment,
                    polarity=sentiment.polarity)
        )

    return bite_sentiments


def _get_average_scores(bite_sentiments):
    average_scores = {}
    for bite_id, comments in sorted(bite_sentiments.items()):
        average_scores[bite_id] = (
            len(comments), mean(c.polarity for c in comments)
        )
    return average_scores


def _show_scores(average_scores):
    print("bite id | # comments | avg sentiment score")
    for bite_id, (num_comments, avg_score) in sorted(
        average_scores.items(), key=lambda x: x[1][1]
    ):
        print(f"{bite_id:7} | {num_comments:10} | {avg_score}")


def show_scores_per_bite():
    feedbacks = _get_feedbacks()
    bite_sentiments = _get_sentiments_per_bite(feedbacks)
    average_scores = _get_average_scores(bite_sentiments)
    _show_scores(average_scores)


def view_feedback_for_bite(bite_id):
    feedbacks = _get_feedbacks()
    bite_sentiments = _get_sentiments_per_bite(feedbacks, bite_id=bite_id)

    try:
        bite_comments = bite_sentiments[bite_id]
    except KeyError:
        print(f"No feedbacks for Bite {bite_id}")
        return None

    for comment in sorted(bite_comments, key=attrgetter('polarity')):
        print(f"{round(comment.polarity, 2):5} | {comment.text}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        bite_id = int(sys.argv[1])
        view_feedback_for_bite(bite_id)
    else:
        show_scores_per_bite()
