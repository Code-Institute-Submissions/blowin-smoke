import os
import datetime
import random
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    """
    The below accesses MongoDB quotes table and gets a
    list of all quotes objects before selecting one
    at random to be shown on page load. Everytime the page
    is refreshed a new random quote will be found.
    """

    single_quote = random.choice(list(mongo.db.quotes.find()))

    context = {
        "quote": single_quote,
    }
    return render_template("index.html", **context)


@app.route("/recipes/")
def recipes():
    """
    A function to render a page of all recipes, with options
    to filter and search.
    """

    recipes = list(mongo.db.quotes.find())

    context = {
        "recipes": recipes,
    }
    return render_template("recipes.html", **context)


def get_current_year():
    """
    Function to return the current year, for use with copyright in footer
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.year


@app.context_processor
def context_processor():
    """
    Context processor for all templates
    """
    return {
        'year': get_current_year
    }


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
