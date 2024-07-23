from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

db = SQLAlchemy()


class Tweet(db.Model):
    __tablename__ = "tweets"

    def __init__(self,
        id: str,
        text: str,
        source: str,
        user_id: str,
        created_at,
        retweeted_status_id: str | None,
        in_reply_to_status_id: str | None,
        in_reply_to_user_id: str | None,
        in_reply_to_screen_name: str | None,
        lang: str,
        retweet_count: int,
        favorite_count: int,
    ) -> None:
        self.id=id
        self.text=text
        self.source=source
        self.user_id=user_id
        self.created_at = created_at
        self.retweeted_status_id = retweeted_status_id
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.lang = lang
        self.retweet_count=retweet_count
        self.favorite_count=favorite_count

    id=db.Column(db.String, primary_key=True, nullable=False, unique=True)
    text=db.Column(db.Text, nullable=False)
    source=db.Column(db.String, nullable=False)
    lang=db.Column(db.String, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    user=db.relationship("User", backref="Tweet", uselist=True)
    retweeted_status_id=db.Column(db.String, db.ForeignKey("tweets.id"), nullable=True)
    retweeted_status = db.relationship("Tweet", uselist=True)
    in_reply_to_status_id = db.Column(db.String, nullable=True)
    in_reply_to_user_id=db.Column(db.String, nullable=True)
    in_reply_to_screen_name=db.Column(db.String, nullable=True)
    retweet_count=db.Column(db.Integer, default=0)
    favorite_count=db.Column(db.Integer,default=0)

    def __str__(self) -> str:
        return f"Text: {self.text}, UserId: {self.user_id}"


class User(db.Model):
    __tablename__="users"

    def __init__(self, id, name, description, screen_name, location,profile_image_url, followers_count, verified, friends_count, created_at) -> None:
        self.id=id
        self.name=name
        self.description = description
        self.screen_name=screen_name
        self.location=location
        self.profile_image_url=profile_image_url
        self.followers_count=followers_count
        self.verified=verified
        self.friends_count= friends_count
        self.created_at = created_at

    id=db.Column(db.String, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.Text)
    screen_name=db.Column(db.String, nullable=False, unique=True)
    location=db.Column(db.String)
    profile_image_url=db.Column(db.String)
    followers_count=db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    verified=db.Column(db.Boolean)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)


    def __str__(self) -> str:
        return f"Name: {self.name}, ScreenName: @{self.screen_name}, Description: {self.description}"


class HashTag(db.Model):

    def __init__(self, text, tweet_id) -> None:
        self.text = text
        self.tweet_id = tweet_id
    __tablename__="hashtags"
    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text=db.Column(db.String, nullable=False)
    tweet_id=db.Column(db.String, db.ForeignKey("tweets.id"), nullable=False)
    tweet=db.relationship("Tweet", backref="HashTag", uselist=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"ID: {self.id}, Text: {self.text}, TweetId: {self.tweet_id}"


class PopularHashTag(db.Model):
    def __init__(self, name: str) -> None:
        self.name = name
    __tablename__="popular_hashtags"

    id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name=db.Column(db.String, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Name: {self.name}"
