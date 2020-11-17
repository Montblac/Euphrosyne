import sys
import praw
from pathlib import Path

from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

BASE_URL = 'https://reddit.com'
MAX_HISTORY = 168
HISTORY_FILENAME = 'history.txt'

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent="Euphrosyne by Montblac")


class Submission:
    def __init__(self, subreddits):
        try:
            if isinstance(subreddits, list):
                self.subreddits = '+'.join(subreddits)
            elif isinstance(subreddits, str):
                self.subreddits = subreddits
            else:
                raise TypeError

            self.history_file = Path(__file__).parent.absolute() / HISTORY_FILENAME
            self.history_data = None
            self.history_idx = None
            self.max_history = MAX_HISTORY

            self.submission = None

            if not self.history_file.exists():
                with open(self.history_file, 'w') as f:
                    f.write('0\n')

        except (TypeError, ValueError) as e:
            print(e)
            sys.exit(0)

    def init_history(self):
        """Reads the history file to get data and last submission index"""
        try:
            with open(self.history_file, 'r') as f:
                self.history_idx = int(f.readline().strip())
                if self.history_idx >= self.max_history:
                    self.history_idx = 0
                self.history_data = f.readlines()

        except ValueError:
            # print('ERROR: Unsuccessful history file read')
            raise ValueError

    def update_history(self):
        """Updates the history file with the latest submission and increments index."""
        if len(self.history_data) < self.max_history:
            self.history_data.append(self.submission.id + '\n')
        else:
            self.history_data[self.history_idx] = self.submission.id + '\n'
            self.history_idx = self.history_idx + 1
        with open(self.history_file, 'w+') as f:
            f.write(str(self.history_idx) + '\n')
            for line in self.history_data:
                f.write(line)

    def get_submission(self):
        """Builds a Subreddit object and retrieves a reddit submission."""
        s = reddit.subreddit(self.subreddits)
        submissions = [s for s in s.hot(limit=50) if not s.stickied and not s.over_18]
        for submission in submissions:
            if submission.id + '\n' in self.history_data:
                continue
            self.submission = submission

    def generate(self):
        """Generates a submission."""
        self.init_history()
        self.get_submission()
        self.update_history()

    def subs(self):
        """Returns a list of all the subreddits used."""
        return self.subreddits.split('+')

    def permalink(self):
        """Returns the full address of the submission."""
        return BASE_URL + self.submission.permalink

    def permalink_short(self):
        """Returns only the permalink portion of submission."""
        return self.submission.permalink

    def url(self):
        """Returns the address of the media accompanying the submission."""
        return self.submission.url
