# socials_api
Methods extract data from principals social networks (Facebook, Twitter, Instagram)

## Twitter 

```
twa = TwitterAPI(consumer_key=consumer_key, consumer_secret=consumer_secret,
                     access_token=access_token, access_token_secret=access_token_secret)


d = twa.get_data_from_username(user_name)
user = TwitterUserHandler(d, id_=1)
user.save_user()
```

## Instagram 

```
scraper = InstagramScraper()
res = scraper.scrap_username(user_name)
user = InstagramUserHandler(res, id_=1)
user.save_user()
```

## Facebook 

```
access_token = app_id + "|" + app_secret
twa = FacebookScraper(access_token=access_token)

d = twa.get_data_from_username(user_name)
if d :
    user = FacebookUserHandler(d, id_=1)
    user.save_user()
else:
    print("UserNotFound")
```
