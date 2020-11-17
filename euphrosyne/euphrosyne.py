from submission import Submission
from tweet import Tweet
from datetime import datetime
from time import sleep

while True:
    time = datetime.now()

    # Check if current time is within 2 minutes of the hour
    if time.minute <= 2 or time.minute >= 58:
        submission = Submission(['aww'])
        submission.generate()

        permalink = submission.permalink()
        url = submission.url()
        permalink_short = submission.permalink_short()

        tweet = Tweet(permalink, url, permalink_short)
        tweet.post()

    print('Trying again after {} minutes.\n'.format(60 - time.minute))
    sleep(60 * (60 - time.minute))
