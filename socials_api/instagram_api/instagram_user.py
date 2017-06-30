from mongoengine import QuerySet

from socials_api.constant import INSTAGRAM_COLLECTION
from socials_api.datamodels.base import MongoSocialInfluencer


class InstagramUserHandler:
    def __init__(self, user, id_):
        self.u = MongoSocialInfluencer(
            id=id_,
            social_id=user["id"],
            username=user["username"],
            description=user["website"],
            followers=user["followers"],
            follows=user["follows"],
            profile_img=user["profile_picture"],
            status_count=user["status_count"],
            posts=user["posts"],
            fulltext=user["fulltext"],
            histogram=user["histogram"],
            twentywords=user["twentywords"],
            tags=user['tags']
        )

    def save_user(self):
        self.u.switch_collection(INSTAGRAM_COLLECTION)
        self.u.save()

    def retreive_all_users(self):
        new_group = MongoSocialInfluencer.switch_collection(MongoSocialInfluencer(), INSTAGRAM_COLLECTION)
        return QuerySet(MongoSocialInfluencer, new_group._get_collection())
