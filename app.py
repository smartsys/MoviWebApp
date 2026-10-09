import os

import requests
from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, url_for
from data_manager import DataManager
from models import db, Movie

load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = os.getenv('OMDB_URL')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/data.db')}"

db.init_app(app)

data_manager = DataManager()

with app.app_context():
    db.create_all()

    # data_manager.create_user('Test User')
    #
    # users = data_manager.get_users()
    # print('get_users:', [(user.id, user.name) for user in users])
    # user = users[-1]
    #
    # data_manager.add_movie(Movie(name='Twister', year=1996, user_id=user.id))
    #
    # movies = data_manager.get_movies(user.id)
    # print('get_movies:', [(movie.id, movie.name) for movie in movies])
    # movie = movies[-1]
    #
    # data_manager.update_movie(movie.id, 'Twister (Updated)')
    # print('update_movie:', [(movie.id, movie.name) for movie in data_manager.get_movies(user.id)])
    #
    # data_manager.delete_movie(movie.id)
    # print('delete_movie:', [(movie.id, movie.name) for movie in data_manager.get_movies(user.id)])


def fetch_movie_data(title, year):
    """Fetch movie details by title and optional year from OMDb."""
    params = {'apikey': OMDB_API_KEY, 't': title}
    if year:
        params['y'] = year
    try:
        response = requests.get(OMDB_URL, params=params, timeout=10)
        return response.json()
    except (requests.RequestException, ValueError):
        return {}


def parse_year(value):
    """Convert a year value to int or return None if it is not a valid year."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@app.route('/')
def index():
    """Show the home page with a list of all users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user and return to the home page."""
    name = request.form['name']
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    """Show a list of a user's favorite movies."""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie with details from OMDb to a user's favorites."""

    title = request.form['title']
    year = request.form.get('year')
    data = fetch_movie_data(title, year)

    if data.get('Response') == 'True':
        print("Response", data.get('Response') )
        movie = Movie(
            name=data['Title'],
            director=data['Director'] if data['Director'] != 'N/A' else None,
            year=parse_year(data['Year'][:4]),
            poster_url=data['Poster'] if data['Poster'] != 'N/A' else None,
            user_id=user_id,
        )
    else:
        print("Response NO")
        movie = Movie(name=title, year=parse_year(year), user_id=user_id)
    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update the title of a movie."""
    movie = data_manager.get_movie(movie_id)
    if movie is None or movie.user_id != user_id:
        abort(404)
    new_title = request.form['title']
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a movie from a user's favorites."""
    movie = data_manager.get_movie(movie_id)
    if movie is None or movie.user_id != user_id:
        abort(404)
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Show the page for unknown URLs."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Show the page for unexpected server errors."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
