import os

from flask import Flask
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/data.db')}"

db.init_app(app)

data_manager = DataManager()

with app.app_context():
    db.create_all()

    data_manager.create_user('Test User')

    users = data_manager.get_users()
    print('get_users:', [(user.id, user.name) for user in users])
    user = users[-1]

    data_manager.add_movie(Movie(name='Twister', year=1996, user_id=user.id))

    movies = data_manager.get_movies(user.id)
    print('get_movies:', [(movie.id, movie.name) for movie in movies])
    movie = movies[-1]

    data_manager.update_movie(movie.id, 'Twister (Updated)')
    print('update_movie:', [(movie.id, movie.name) for movie in data_manager.get_movies(user.id)])

    data_manager.delete_movie(movie.id)
    print('delete_movie:', [(movie.id, movie.name) for movie in data_manager.get_movies(user.id)])


@app.route('/')
def home():
    """Show a welcome message."""
    return "Welcome to MoviWeb App!"


if __name__ == '__main__':
    app.run()
