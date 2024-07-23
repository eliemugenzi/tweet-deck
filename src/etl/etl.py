import json

from ..serializers.serializer import TweetSerializer
from ..models.models import HashTag, Tweet, User, db
import pandas as pd

class ETL:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path


    def convert_data_to_json(self, ddd):
       return json.loads(ddd)


    def serialize_data(self, dataset) -> list[TweetSerializer]:
        tweet_serializer_list: list[TweetSerializer] = []
        for data in dataset:
            hashtag_list: list[HashTag] = []
            retweeted_hashtag_list: list[HashTag] = []
            if data["user"]:
                user = User(
                    id=data["user"]["id_str"],
                    name=data["user"]["name"],
                    screen_name=data["user"]["screen_name"],
                    profile_image_url=data["user"]["profile_image_url"],
                    description=data["user"]["description"],
                    followers_count=data["user"]["followers_count"],
                    location=data["user"]["location"],
                    verified=data["user"]["verified"],
                    friends_count=data["user"]["friends_count"],
                    created_at=data["user"]["created_at"]
                )

            if data["entities"] != None:
                entities = dict(data["entities"])
                hashtags = entities["hashtags"]

                for hashtag in hashtags:
                    hash = HashTag(text=hashtag["text"], tweet_id=data["id_str"])
                    hashtag_list.append(hash)

            print(f"Retweeted Status: {data}")
            retweeted_status: Tweet | None = None
            retweeted_user: User | None = None
            if "retweeted_status" in data:
                retweeted_user = User(
                    id=data["retweeted_status"]["user"]["id_str"],
                    name=data["retweeted_status"]["user"]["name"],
                    screen_name=data["retweeted_status"]["user"]["screen_name"],
                    profile_image_url=data["retweeted_status"]["user"]["profile_image_url"],
                    description=data["retweeted_status"]["user"]["description"],
                    followers_count=data["retweeted_status"]["user"]["followers_count"],
                    location=data["retweeted_status"]["user"]["location"],
                    verified=data["retweeted_status"]["user"]["verified"],
                    friends_count=data["retweeted_status"]["user"]["friends_count"],
                    created_at=data["retweeted_status"]["user"]["created_at"]
                )

                retweet_hashtags = data["retweeted_status"]["entities"]["hashtags"]
                retweeted_hashtag_list: list[HashTag] = []
                for retweet_hashtag in retweet_hashtags:
                    hashtag = HashTag(text=retweet_hashtag["text"], tweet_id=data["retweeted_status"]["id_str"])
                    retweeted_hashtag_list.append(hashtag)


                retweeted_status = Tweet(
                    id=data["retweeted_status"]["id_str"],
                    source=data["retweeted_status"]["source"],
                    lang=data["retweeted_status"]["lang"],
                    text=data["retweeted_status"]["text"],
                    user_id=retweeted_user.id,
                    retweeted_status_id=None,
                    in_reply_to_status_id=data["retweeted_status"]["in_reply_to_status_id"],
                    in_reply_to_user_id=data["retweeted_status"]["in_reply_to_user_id"],
                    in_reply_to_screen_name=data["retweeted_status"]["in_reply_to_screen_name"],
                    created_at=data["retweeted_status"]["created_at"],
                    retweet_count=data["retweeted_status"]["retweet_count"],
                    favorite_count=data["retweeted_status"]["favorite_count"]
                )

            tweet_serializer = TweetSerializer(
                id=data["id_str"],
                source=data["source"],
                text=data["text"],
                user=user,
                hashtags=hashtag_list,
                created_at=data["created_at"],
                in_reply_to_user_id=data["in_reply_to_user_id"],
                in_reply_to_status_id=data["in_reply_to_status_id"],
                in_reply_to_screen_name=data["in_reply_to_screen_name"],
                retweeted_status=retweeted_status,
                lang=data["lang"],
                retweeted_user=retweeted_user,
                retweet_count=data["retweet_count"],
                favorite_count=data["favorite_count"],
                retweet_hashtags=retweeted_hashtag_list if "retweeted_status" in data else None
            )
            tweet_serializer_list.append(tweet_serializer)
        return tweet_serializer_list


    def filter_data(self, dataset):
        if dataset["id"] != None:
            return True
        elif dataset["id_str"] != None:
            return True
        elif dataset["entities"] != None:
            return True
        elif (dataset["lang"] == "en"
            or dataset["lang"] == "ar"
            or dataset["lang"] == "fr"
            or dataset["lang"] == "in"
            or dataset["lang"] == "pt"
            or dataset["lang"] == "es"
            or dataset["lang"] == "tr"
            or dataset["lang"] == "ja"
        ):
            return True
        return False

    def transform_data(self, raw_data: list[str]):
        dataset = filter(self.filter_data, raw_data)
        return self.serialize_data(list(dataset))

    def load_data_to_csv(self, dataframe, output_path):
        dataframe.to_csv(output_path, index = False)

    def extract_data_from_file(self) -> list[str]:
        with open(self.file_path, 'r') as file:
            itemList = file.readlines()
            data = list(map(self.convert_data_to_json, itemList))
        return data

    def load_to_warehouse(self, dataset: list[TweetSerializer]):
        for tweet in dataset:
            user = tweet.user
            retweet_status = tweet.retweeted_status
            retweeted_user = tweet.retweeted_user

            if retweet_status != None:
                already_existing_tweet = Tweet.query.filter_by(id=retweet_status.id).first()
                if already_existing_tweet == None:
                    already_exist_user = User.query.filter_by(id=retweet_status.user_id).first()
                    if already_exist_user == None:
                        db.session.add(retweeted_user)
                        db.session.commit()
                    t_data = Tweet(
                        id=retweet_status.id,
                        user_id= retweet_status.user_id,
                        source=retweet_status.source,
                        created_at = retweet_status.created_at,
                        text=retweet_status.text,
                        in_reply_to_user_id=retweet_status.in_reply_to_user_id,
                        in_reply_to_status_id=retweet_status.in_reply_to_status_id,
                        in_reply_to_screen_name=retweet_status.in_reply_to_screen_name,
                        lang=retweet_status.lang,
                        retweeted_status_id=None,
                        favorite_count=retweet_status.favorite_count,
                        retweet_count=retweet_status.retweet_count
                    )

                    db.session.add(t_data)
            tweet_data = Tweet(id=tweet.id,
                text=tweet.text,
                source=tweet.source,
                user_id=user.id,
                created_at=tweet.created_at,
                retweeted_status_id=retweet_status.id if retweet_status != None else None,
                lang=tweet.lang,
                in_reply_to_user_id=tweet.in_reply_to_user_id,
                in_reply_to_status_id=tweet.in_reply_to_status_id,
                in_reply_to_screen_name=tweet.in_reply_to_screen_name,
                favorite_count=tweet.favorite_count,
                retweet_count=tweet.retweet_count
            )
            print(f"Tweet Data: {tweet_data}")
            existing_user = User.query.filter_by(id=user.id).first()
            existing_tweet = Tweet.query.filter_by(id=tweet.id).first()
            if existing_user == None:
                db.session.add(user)
            if existing_tweet == None:
                db.session.add(tweet_data)
            db.session.commit()

            for hashtag in tweet.hashtags:
                hashtag_data = HashTag(text=hashtag.text, tweet_id=tweet_data.id)
                db.session.add(hashtag_data)
                db.session.commit()
