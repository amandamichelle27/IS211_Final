# Third-party imports.
from flask import Flask

# Basic configuration for the app to be re-used across components.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "thisissecret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False