from praw import Reddit
from pathlib import Path

reddit = Reddit('AwwBot')
subreddit = reddit.subreddit('aww')

# create a text file to store recently tweeted submissions
# use header for index of last submission entry modified
history = Path('history.txt')
max_history = 3 #168
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

    # TODO: tweet submission.url/submission.permalink

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
