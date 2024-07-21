from src.etl.etl import ETL
from flask import Flask
import pandas as pd
import json
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()


app = Flask(__name__)
CORS(app)

def run_etl():
    etl_l = ETL("./src/query2_ref.txt")
    data_1 = etl_l.extract_data_from_file()
    data_2 = etl_l.transform_data(data_1)

    print(f"Data transformed___: {data_2[4]}")


if __name__ == "__main__":
    run_etl()
    app.run(debug=True)
