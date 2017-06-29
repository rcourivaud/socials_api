from mongoengine import fields, EmbeddedDocument, Document, connect

from socials_api.constant import MONGO_URL, MONGO_PORT

connect(db='influencers', host=MONGO_URL, port=MONGO_PORT, username='admin', password='Influstein17')


class MongoPost(EmbeddedDocument):
    id = fields.IntField(required=True)
    likes = fields.IntField()
    date = fields.DateTimeField()
    text = fields.StringField()
    img = fields.StringField()


class MongoSocialInfluencer(Document):
    id = fields.IntField(primary_key=True)
    social_id = fields.IntField()
    username = fields.StringField()
    description = fields.StringField()
    followers = fields.IntField()
    follows = fields.IntField()
    profile_img = fields.StringField()
    status_count = fields.IntField()
    posts = fields.ListField(type=MongoPost)
    fulltext = fields.StringField()
    histogram = fields.DictField()
    twentywords = fields.ListField()
    tags = fields.ListField()




