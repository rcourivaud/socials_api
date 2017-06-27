import time
import tweepy

from datamodels.base import save_twitter
from meta_extractor import HistExtractor
from twitter_api.twitter_user import TwitterUserHandler


class TwitterAPI:
    def __init__(self, consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth)
        self.histgram_extractor = HistExtractor()


    def get_user_by_name(self, user_name):
        try:
            return self.api.get_user(user_name)
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

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
        result_dict["fulltext"] = " ".join([elt["text"] for elt in result_dict['posts']])

        result_dict["histogram"] = self.histgram_extractor.get_histogram_from_string(result_dict["fulltext"])
        result_dict["twentywords"] = [k for k, v in sorted(result_dict["histogram"].items(),
                                                           key=lambda x: x[1], reverse=True) ][0:20]

        return result_dict

    def get_data_from_username(self, username):
        d = self.get_data(self.get_user_by_name(user_name=username))
        return d

if __name__ =="__main__":
    consumer_key = "KlPIWgeCoUhrk4xe7VkqQZHmV"
    consumer_secret = "kr0G5mHe2WTyS844Fclm3ewz09Jt8mXJbdvJUQQDoSQibfTcaM"
    access_token = "592331421-dG45Iu4twLcbrIELIi2qHC6u8x9levwT8PYhqFfy"
    access_token_secret = "gDSn3Rs0U4qd8vOkhUasjXjvvP21fWX8cw2Qp1Qo7rsC2"
    twa = TwitterAPI(consumer_key=consumer_key, consumer_secret=consumer_secret,
                     access_token=access_token, access_token_secret=access_token_secret)


    d = twa.get_data_from_username("influenzzzfr")
    TwitterUserHandler(d, id_=1)
