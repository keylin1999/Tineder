# return db for development testing

from flask import Flask
from config import app_load_config
from model import db

app = Flask(__name__)
app_load_config(app)
db.app = app
db.init_app(app)