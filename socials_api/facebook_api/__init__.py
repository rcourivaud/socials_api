import json

import requests

from socials_api.meta_extractor import MetaExtractor


class FacebookScraper:
    def __init__(self, access_token):
        self.base_url = "https://graph.facebook.com/v2.9/"
        self.access_token = access_token
        self.meta_extractor = MetaExtractor()

    def get_facebook_page_id_from_name(self, name):
        # construct the URL string
        base = "https://graph.facebook.com/v2.4"
        node = "/" + name
        parameters = "/?access_token=%s" % self.access_token
        url = base + node + parameters

        # retrieve data
        response = requests.get(url)
        data = json.loads(response.text)

        return data.get("id")

    def get_facebook_page_data(self, page_id):
        # construct the URL string
        parameters = "?fields=about,posts.limit(100){message,link,likes,created_time}," \
                     "fan_count,picture&access_token=%s" % self.access_token  # changed
        url = self.base_url + page_id + parameters

        # retrieve data
        data = json.loads(requests.get(url).text)

        return data

    def get_data_from_username(self, username):
        user_id = self.get_facebook_page_id_from_name(name=username)
        if user_id:
            data = self.get_facebook_page_data(page_id=user_id)
            result_dict = {"description": data.get('about'), "followers": data.get("fan_count"),
                           "profile_img": data["picture"]["data"]["url"] if data.get("picture") else None,
                           "social_id": data["id"],
                           "posts": [{k: v for k, v in {
                               "id": elt["id"],
                               "text": elt.get("message"),
                               "img": elt.get("link"),
                               "likes": len(elt["likes"]["data"]) if elt.get("likes") else 0,
                               "date": elt["created_time"]
                           }.items() if v} for elt in data["posts"]["data"]], "username": username}

            result_dict["fulltext"] = " ".join([elt["text"] for elt in result_dict['posts'] if elt.get("text")]).replace("\n", " ")

            result_dict["histogram"] = self.meta_extractor.get_histogram_from_string(result_dict["fulltext"])
            result_dict["twentywords"] = [k for k, v in sorted(result_dict["histogram"].items(),
                                                               key=lambda x: x[1], reverse=True)][0:20]
            result_dict["tags"] = self.meta_extractor.get_hashtags_from_string(result_dict["fulltext"])
            return {k: v for k, v in result_dict.items() if v}
        return None