from flask import Blueprint, request

from ..models.models import Tweet

q2_blueprint = Blueprint("q2", __name__)

@q2_blueprint.route("/", methods=["GET"])
def index():
    query_params = request.args
    params_dict = query_params.to_dict()
    print(f"Request: {params_dict['type']}")

    tweets=[]

    if params_dict["type"] == "reply":
        tweets = Tweet.query.filter(
            Tweet.in_reply_to_user_id.isnot(None),
            Tweet.in_reply_to_screen_name.isnot(None),
            Tweet.in_reply_to_status_id.isnot(None)
        ).all()
        print(f"Tweets: {tweets[1]}")

    return "I am HIM"
