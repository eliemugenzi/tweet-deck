# Tweet Deck
> This is a User recommendation system based on Twitter Data

## Getting started

- Make sure you have Python installed on your computer
- Clone this repository, cd into it
- Create a python virtual environment by running the command `virtualenv venv` and activate it using `source venv/bin/activate`
- Move the text files `query2_ref.txt` and `popular_hashtags.txt` in src folder
- Install the project dependencies using `pip3 install -r requirements.txt`
- Create the `.env` file in the root directory and populate the data according to `.env.example` file to setup the database url and secret key.
- To have the database schema up to date, you will need to run the command `flask db upgrade`
