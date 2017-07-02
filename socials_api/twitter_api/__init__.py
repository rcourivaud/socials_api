import time

import tweepy

from socials_api.constant import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from socials_api.meta_extractor import MetaExtractor
from socials_api.twitter_api.twitter_user import TwitterUserHandler


class TwitterAPI:
    def __init__(self, consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth)
        self.meta_extractor = MetaExtractor()

    def get_user_by_name(self, user_name):
        try:
            return self.api.get_user(user_name)
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
        except tweepy.RateLimitError:
            return None

    def get_data(self, twitter_user):
        result_dict = {
            "description": twitter_user.description,
            "profile_img": twitter_user.profile_image_url,
            "followers": twitter_user.followers_count,
            "location": twitter_user.location,
            "social_id": twitter_user.id,
            "follows": twitter_user.friends_count,
            "created_date": twitter_user.created_at,
            "username": twitter_user.name,
            "status_count": twitter_user.statuses_count,
            "posts": [{
                           "id": elt.id,
                           "text": elt.text,
                           "likes": elt.retweet_count,
                           "date": elt.created_at,
                       } for elt in twitter_user.timeline(count=200) if not elt.retweeted],
        }
        result_dict["fulltext"] = " ".join([elt["text"] for elt in result_dict['posts']]).replace("\n", " ")

        result_dict["histogram"] = self.meta_extractor.get_histogram_from_string(result_dict["fulltext"])
        result_dict["twentywords"] = [k for k, v in sorted(result_dict["histogram"].items(),
                                                           key=lambda x: x[1], reverse=True) ][0:20]
        result_dict["tags"] = self.meta_extractor.get_hashtags_from_string(result_dict["fulltext"])
        return result_dict

    def get_data_from_username(self, username):
        d = self.get_data(self.get_user_by_name(user_name=username))
        return d

if __name__ =="__main__":
    twa = TwitterAPI(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                     access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


    d = twa.get_data_from_username("influenzzzfr")
    TwitterUserHandler(d, id_=1)
