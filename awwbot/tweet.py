import os
import sys
import time
import requests
from pathlib import Path
from requests_oauthlib import OAuth1

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

# Configure environment variables
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

oauth = OAuth1(
    client_key=TWITTER_CONSUMER_KEY,
    client_secret=TWITTER_CONSUMER_SECRET,
    resource_owner_key=TWITTER_ACCESS_TOKEN,
    resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET
)


class Tweet:
    def __init__(self, status, media_url=None, permalink=None):
        self.status = status
        self.media_url = media_url
        self.permalink = permalink

        self.media_id = None
        self.media_type = None
        self.total_bytes = 0
        self.processing_info = None
        self.temp_file = None

        self.supported_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mpeg']
        self.supported_types = ['image', 'video']

    def media_download(self):
        """Downloads the content from the media url locally."""
        # TODO: Improve and clean error-checking for failed media download
        print('DOWNLOADING MEDIA.')
        request = requests.get(self.media_url, stream=True)
        self.media_type = request.headers['content-type'].split('/')
        self.temp_file = Path('temp.' + self.media_type[1])

        if request.status_code == 200:
            if self.media_type[0] in self.supported_types and self.media_type[1] in self.supported_formats:
                with open(str(self.temp_file), 'wb') as file:
                    for chunk in request:
                        file.write(chunk)

                self.total_bytes = self.temp_file.stat().st_size

                print('DOWNLOADED MEDIA SUCCESSFULLY.')
                return request.status_code

            print("DOWNLOADING MEDIA FAILED: Unsupported Media Type")

        print("DOWNLOADING MEDIA FAILED: STATUS_CODE ", request.status_code)
        sys.exit(0)

    def upload_init(self):
        """Initializes media upload."""
        print('INITIALIZING FILE UPLOAD.')
        request_data = {
            'command': 'INIT',
            'total_bytes': self.total_bytes,
            'media_type': self.media_type
        }
        request = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
        self.media_id = request.json()['media_id']
        print('UPLOAD INITIALIZATION COMPLETED.')

    def upload_append(self):
        """Uploads media in chunks and appends to chunks uploaded."""
        print('UPLOADING MEDIA IN CHUNKS.')
        segment_id = 0
        bytes_sent = 0
        file = open(self.temp_file, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4*1024*1024)
            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }
            files = {
                'media': chunk
            }
            request = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

            if request.status_code < 200 or request.status_code > 299:
                sys.exit(0)

            segment_id = segment_id + 1
            bytes_sent = file.tell()

            print('* {} of {} bytes uploaded'.format(bytes_sent, self.total_bytes))

        print('CHUNK UPLOAD COMPLETED.')

    def upload_finalize(self):
        """Finalizes media upload."""
        print('FINALIZING MEDIA UPLOAD')
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        request = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)

        self.processing_info = request.json().get('processing_info', None)
        self.check_status()
        print('UPLOAD FINALIZATION COMPLETED.')

    def check_status(self):
        """Checks video processing status."""
        if self.processing_info is None:
            return

        state = self.processing_info['state']
        print('Media processing status {} '.format(state))

        if state == 'succeeded':
            return

        if state == 'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after {} seconds'.format(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        request = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)

        self.processing_info = request.json().get('processing_info', None)
        self.check_status()

    def post(self):
        """ Publishes tweet """
        print('PROCESSING TWEET TO PUBLISH')
        self.media_download()
        self.upload_init()
        self.upload_append()
        self.upload_finalize()
        self.temp_file.unlink()

        request_data = {
            'status': self.status,
            'media_ids': self.media_id
        }

        requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)
        print('TWEET POSTED!')
