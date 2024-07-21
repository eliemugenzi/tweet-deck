from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()


class Tweet(db.Model):
    __tablename__ = "tweets"
    id=db.Column(db.String, primary_key=True, nullable=False, unique=True)
    text=db.Column(db.Text, nullable=False)
    source=db.Column(db.String, nullable=False)
    user_id=db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    user=db.relationship("User", backref="Tweet", uselist=True)

    def __str__(self) -> str:
        return f"Text: {self.text}, UserId: {self.user_id}"


class User(db.Model):
    __tablename__="users"

    def __init__(self, id, name, description, screen_name, location,profile_image_url, followers_count, verified) -> None:
        self.id=id
        self.name=name
        self.description = description
        self.screen_name=screen_name
        self.location=location
        self.profile_image_url=profile_image_url
        self.followers_count=followers_count
        self.verified=verified

    id=db.Column(db.String, primary_key=True, unique=True, nullable=False)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.Text)
    screen_name=db.Column(db.String, nullable=False, unique=True)
    location=db.Column(db.String)
    profile_image_url=db.Column(db.String)
    followers_count=db.Column(db.Integer)
    friends_count = db.Column(db.Integer)
    verified=db.Column(db.Boolean)

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

    def __str__(self) -> str:
        return f"ID: {self.id}, Text: {self.text}, TweetId: {self.tweet_id}"
