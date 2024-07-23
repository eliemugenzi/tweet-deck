from src.etl.popular_hashtags import load_popular_hashtags
from src.etl.etl import ETL
from flask import Flask, Blueprint
import pandas as pd
import json
from os import environ as Env
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.models import models
from src.blueprints.q2 import q2_blueprint

load_dotenv()

DATABASE_URL = Env.get("DATABASE_URL")
SECRET_KEY = Env.get("SECRET_KEY")
app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(q2_blueprint, url_prefix="/q2")

migrate = Migrate(app, models.db)
models.db.init_app(app)

def run_etl():
    tweets_data = models.User.query.all()
    if len(tweets_data) != 0:
        return

    load_popular_hashtags("./src/popular_hashtags.txt")
    etl_instance = ETL("./src/query2_ref.txt")
    data_1 = etl_instance.extract_data_from_file()
    data_2 = etl_instance.transform_data(data_1)

    etl_instance.load_to_warehouse(data_2)

if __name__ == "__main__":
    with app.app_context():
        run_etl()
    app.run(debug=True)
