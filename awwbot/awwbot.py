import os
from pathlib import Path

import praw

from tweet import Tweet

# initialize api keys from environment variables
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

# reddit authentication
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent="AwwBot by Montblac")
subreddit = reddit.subreddit('aww')
base_url = 'https://reddit.com'

# create a text file to store recently tweeted submissions
# use header for index of last submission entry modified
history = Path('history.txt')
max_history = 168
if not history.exists():
    with open(history, 'w') as f:
        f.write('0\n')

with open(history, 'r') as f:
    try:
        index = int(f.readline().strip())
        if index >= max_history:
            index = 0
        data = f.readlines()
    except ValueError:
        raise ValueError

submissions = [submission for submission in subreddit.hot(limit=50) if not submission.stickied and not submission.over_18]
for submission in submissions:
    if submission.id + '\n' in data:
        continue

    try:
        tweet = Tweet(base_url + submission.permalink, submission.url, submission.permalink)
        tweet.post()

    except SystemExit:
        print()
        continue

    if len(data) < max_history:
        data.append(submission.id + '\n')
    else:
        data[index] = submission.id + '\n'
        index += 1
    with open(history, 'w+') as f:
        f.write(str(index) + '\n')
        for line in data:
            f.write(line)
    break
