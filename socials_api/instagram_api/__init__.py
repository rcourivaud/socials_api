import datetime
import json
import logging.config
import os
import re
import sys
import textwrap
import time
import warnings
import requests
import tqdm
from bson import json_util

from instagram_scraper.constants import *

warnings.filterwarnings('ignore')


class InstagramScraper(object):
    """InstagramScraper scrapes and downloads an instagram user's photos and videos"""

    def __init__(self, **kwargs):
        default_attr = dict(username='', usernames=[], filename=None,
                            login_user=None, login_pass=None,
                            destination='./', retain_username=False,
                            quiet=False, maximum=0, media_metadata=False, latest=False,
                            media_types=['image', 'video', 'story'], tag=False, location=False,
                            search_location=False, comments=False)

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = kwargs.get(key)

        # Set up a file logger
        self.logger = InstagramScraper.get_logger(level=logging.WARN)

        self.posts = []
        self.session = requests.Session()
        self.cookies = None
        self.logged_in = False
        self.last_scraped_filemtime = 0

    def login(self):
        """Logs in to instagram."""
        self.session.headers.update({'Referer': BASE_URL})
        req = self.session.get(BASE_URL)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login_data = {'username': self.login_user, 'password': self.login_pass}
        login = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies

        if login.status_code == 200 and json.loads(login.text)['authenticated']:
            self.logged_in = True
        else:
            self.logger.exception('Login failed for ' + self.login_user)
            raise ValueError('Login failed for ' + self.login_user)

    def logout(self):
        """Logs out of instagram."""
        if self.logged_in:
            try:
                logout_data = {'csrfmiddlewaretoken': self.cookies['csrftoken']}
                self.session.post(LOGOUT_URL, data=logout_data)
                self.logged_in = False
            except requests.exceptions.RequestException:
                self.logger.warning('Failed to log out ' + self.login_user)

    def scrap_username(self, username):
        self.posts = []
        self.last_scraped_filemtime = 0
        future_to_item = {}

        # Get the user metadata.
        user = self.fetch_user(username)
        self.logger.info("fetch {} user".format(username))
        return json.dumps(self.extract_data(user), default=json_util.default, ensure_ascii=False)

    def extract_data(self, response):
        return {
            "profile_picture": response["profile_pic_url_hd"],
            "username": response["username"],
            "full_name": response["full_name"],
            "is_verified": response["is_verified"],
            "followers": response['followed_by']["count"],
            "website": response['external_url'],
            "follows": response["follows"]["count"],
            "id": response["id"],
            "posts": [self.clean_post(post) for post in response["media"]["nodes"]],
            "time":datetime.datetime.now()

        }

    def clean_post(self, post):
        """

        :param post:
        :return:

        Exemple : {'owner': {'id': '2214692775'}, 'likes': {'count': 11}, '__typename': 'GraphImage',
            'comments': {'count': 1}, 'gating_info': None, 'comments_disabled': False,
            'dimensions': {'height': 1080, 'width': 1080}, 'id': '1543511197109075045',
            'display_src': 'https://scontent-cdg2-1.cdninstagram.com/t51.2885-15/e35/19367855_143548912871351_2927919883318460416_n.jpg',
            'date': 1498220894, 'caption': 'Un remerciement officiel pour notre correcteur personnel ! \n#instablog #motdujour #grammarnazi #correction #correcteur #faute #orthographe\nCc @mamougram',
            'is_video': False, 'thumbnail_src': 'https://scontent-cdg2-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/19367855_143548912871351_2927919883318460416_n.jpg',
            'media_preview': None, 'code': 'BVrp0GChjxl'}
        """

        f_dict = {
            "likes": post['likes']["count"],
            "id": post["id"],
            "img": post["display_src"],
            "date": self.get_date_from_timestamp(post["date"]),
            "text": post.get("caption", None),
        }
        return {k: v for k, v in f_dict.items() if v}

    @staticmethod
    def get_date_from_timestamp(d):
        """

        :param d:
        :return:
        """
        return datetime.datetime.fromtimestamp(d)

    def fetch_user(self, username):
        """Fetches the user's metadata."""
        resp = self.session.get(BASE_URL + username)

        if resp.status_code == 200 and '_sharedData' in resp.text:
            try:
                shared_data = resp.text.split("window._sharedData = ")[1].split(";</script>")[0]
                return json.loads(shared_data)['entry_data']['ProfilePage'][0]['user']
            except (TypeError, KeyError, IndexError):
                pass

    @staticmethod
    def get_logger(level=logging.WARNING, log_file='instagram-scraper.log'):
        """Returns a file logger."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.NOTSET)

        handler = logging.FileHandler(log_file, 'w')
        handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

if __name__ == "__main__":
    scraper = InstagramScraper()
    print(scraper.scrap_username("influenzzz"))
