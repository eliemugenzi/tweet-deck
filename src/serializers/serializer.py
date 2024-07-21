from ..models.models import User, HashTag


class TweetSerializer:
    def __init__(self, id: str, text: str, source: str, user: User, hashtags: list[HashTag]) -> None:
        self.id=id
        self.text=text
        self.source=source
        self.user=user
        self.hashtags=hashtags


    def __str__(self) -> str:
        return f"ID: {self.id}, Text: {self.text}, User: {self.user}, HashTags: {self.hashtags}"
