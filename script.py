from collections import defaultdict
import os
from statistics import mean

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from textblob import TextBlob

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])
session = sessionmaker(engine)()

# https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html
metadata = MetaData()
metadata.reflect(engine, only=['bites_bite', 'bites_biteconsumer'])

Base = automap_base(metadata=metadata)
Base.prepare()

table = Base.classes.bites_biteconsumer


def _get_feedbacks():
    feedbacks = session.query(table.bite_id, table.comments).filter(
        and_(table.comments != None, table.comments != '')  # noqa E711
    )
    return feedbacks


def main(negative_only=True):
    feedbacks = _get_feedbacks()

    results = defaultdict(list)
    for feedback in feedbacks.all():
        bite_id, comment = feedback
        sentiment = TextBlob(comment).sentiment
        results[bite_id].append(sentiment.polarity)

    average_scores = {}
    for bite_id, scores in sorted(results.items()):
        average_scores[bite_id] = len(scores), mean(scores)

    print("bite id | # comments | avg sentiment score")
    for bite_id, (num_comments, avg_score) in sorted(
        average_scores.items(), key=lambda x: x[1][1]
    ):
        if negative_only and avg_score >= 0:
            continue
        print(f"{bite_id:7} | {num_comments:10} | {avg_score}")


def view_comments_bite(bite_id):
    feedbacks = _get_feedbacks()
    bite_comments = feedbacks.filter(table.bite_id == bite_id).all()
    for row in bite_comments:
        comment = row[1]
        sentiment = TextBlob(comment).sentiment
        print(sentiment.polarity, comment)


if __name__ == "__main__":
    main()
