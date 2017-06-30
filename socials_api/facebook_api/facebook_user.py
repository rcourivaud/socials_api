from mongoengine import QuerySet

from socials_api.constant import FACEBOOK_COLLECTION
from socials_api.datamodels.base import MongoSocialInfluencer


class FacebookUserHandler:
    def __init__(self, user, id_):
        self.u = MongoSocialInfluencer(
            id=id_,
            social_id=user["social_id"],
            username=user["username"],
            description=user["description"],
            followers=user["followers"],
            profile_img=user["profile_img"],
            posts=user["posts"],
            fulltext=user["fulltext"],
            histogram=user["histogram"],
            twentywords=user["twentywords"],
            tags=user['tags']
        )

    def save_user(self):
        self.u.switch_collection(FACEBOOK_COLLECTION)
        self.u.save()

    def retreive_all_users(self):
        new_group = MongoSocialInfluencer.switch_collection(MongoSocialInfluencer(), FACEBOOK_COLLECTION)
        return QuerySet(MongoSocialInfluencer, new_group._get_collection())
