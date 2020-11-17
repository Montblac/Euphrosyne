from tweet import Tweet
from submission import Submission

try:
    submission = Submission(['aww'])
    submission.generate()

    permalink = submission.permalink()
    url = submission.url()
    permalink_short = submission.permalink_short()

    tweet = Tweet(permalink, url, permalink_short)
    tweet.post()

except SystemExit:
    print()
