from praw import Reddit
from pathlib import Path
from credentials import *
import tweepy
import requests

base_url = 'https://reddit.com'
reddit = Reddit('AwwBot')
subreddit = reddit.subreddit('aww')

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

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
        request = requests.get(submission.url, stream=True)
        if request.status_code == 200:
            status = base_url + submission.permalink
            print('Processing:', status)

            file = Path('temp.jpg')
            if Path(submission.url).suffix in ['.jpeg', '.jpg', '.png']:
                with open(str(file), 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                media = api.media_upload(str(file))
                api.update_status(status=status, media_ids=[media.media_id])
                file.unlink()
            else:
                api.update_status(status)
        else:
            continue
    except:
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
