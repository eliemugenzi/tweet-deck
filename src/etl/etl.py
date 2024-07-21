import json

from ..serializers.serializer import TweetSerializer
from ..models.models import HashTag, User
import pandas as pd

class ETL:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path


    def convert_data_to_json(self, ddd):
       return json.loads(ddd)


    def transform_data_into_objects(self, dataset) -> list[TweetSerializer]:
        tweet_serializer_list: list[TweetSerializer] = []
        for data in dataset:
            hashtag_list: list[HashTag] = []
            if data["user"]:
                user = User(
                    id=data["user"]["id"],
                    name=data["user"]["name"],
                    screen_name=data["user"]["screen_name"],
                    profile_image_url=data["user"]["profile_image_url"],
                    description=data["user"]["description"],
                    followers_count=data["user"]["followers_count"],
                    location=data["user"]["location"],
                    verified=data["user"]["verified"]
                )

            if data["entities"] != None:
                entities = dict(data["entities"])
                hashtags = entities["hashtags"]

                for hashtag in hashtags:
                    hash = HashTag(text=hashtag["text"], tweet_id=data["id_str"])
                    hashtag_list.append(hash)

            tweet_serializer = TweetSerializer(id=data["id"], source=data["source"], text=data["text"], user=user, hashtags=hashtag_list)
            tweet_serializer_list.append(tweet_serializer)
        return tweet_serializer_list


    def clean_data(self, dataset):
        if dataset["id"] == None or dataset["id_str"] == None:
            return False
        elif dataset["entities"] != None:
            return True
        return True

    def transform_data(self, raw_data: list[str]):
        dataset = filter(self.clean_data, raw_data)
        return self.transform_data_into_objects(raw_data)

    def load_data_to_csv(self, dataframe, output_path):
        dataframe.to_csv(output_path, index = False)

    def extract_data_from_file(self) -> list[str]:
        with open(self.file_path, 'r') as file:
            itemList = file.readlines()
            data = list(map(self.convert_data_to_json, itemList))
        return data

    def load_to_warehouse(self, dataset):
        pass
