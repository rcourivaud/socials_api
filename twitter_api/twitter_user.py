from mongoengine import connect
from mongoengine.context_managers import switch_collection

from constant import TWITTER_COLLECTION, MONGO_URL, MONGO_PORT
from datamodels.base import MongoSocialInfluencer
from mongoengine.queryset import QuerySet


class TwitterUserHandler:
    def __init__(self, user, id_):
        self.u = MongoSocialInfluencer(
            id=id_,
            social_id=user["social_id"],
            username=user["username"],
            description=user["description"],
            followers=user["followers"],
            follows=user["follows"],
            profile_img=user["profile_img"],
            status_count=user["status_count"],
            posts=user["posts"],
            fulltext=user["fulltext"],
            histogram=user["histogram"],
            twentybestswords=user["twentywords"]
        )

    def save_user(self):
        self.u.switch_collection(TWITTER_COLLECTION)
        self.u.save()

    def retreive_all_users(self):
        new_group = MongoSocialInfluencer.switch_collection(MongoSocialInfluencer(), TWITTER_COLLECTION)
        return QuerySet(MongoSocialInfluencer, new_group._get_collection())
