import os

from flask import Flask
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/data.db')}"

db.init_app(app)

with app.app_context():
    db.create_all()
