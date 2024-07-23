from ..models.models import Tweet, User, HashTag


class TweetSerializer:
    def __init__(self,
        id: str,
        text: str,
        source: str,
        user: User,
        hashtags: list[HashTag],
        created_at,
        in_reply_to_status_id: str | None,
        in_reply_to_user_id: str | None,
        in_reply_to_screen_name: str | None,
        retweeted_status: Tweet | None,
        lang: str,
        retweeted_user: User | None,
        retweet_count: int,
        favorite_count: int,
        retweet_hashtags: list[HashTag] | None
    ) -> None:
        self.id=id
        self.text=text
        self.source=source
        self.user=user
        self.hashtags=hashtags
        self.created_at=created_at
        self.retweeted_status = retweeted_status
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.lang = lang
        self.retweeted_user = retweeted_user
        self.retweet_count=retweet_count
        self.favorite_count= favorite_count
        self.retweet_hashtags=retweet_hashtags


    def __str__(self) -> str:
        return f"ID: {self.id}, Text: {self.text}, User: {self.user}, HashTags: {self.hashtags}"
