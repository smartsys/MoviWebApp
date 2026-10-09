import os

from flask import Flask, redirect, render_template, request, url_for
from data_manager import DataManager
from models import db, Movie

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


@app.route('/')
def index():
    """Show the home page with a list of all users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users')
def list_users():
    """Return all users as a string."""
    users = data_manager.get_users()
    for user in users:
        print(users)

    return str(users)  # Temporarily returning users as a string


@app.route('/users/<int:user_id>/movies')
def get_movies(user_id):
    """Show a list of a user's favorite movies."""
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie with title and optional year to a user's favorites."""
    title = request.form['title']
    year = request.form.get('year')
    movie = Movie(name=title, year=int(year) if year else None, user_id=user_id)
    data_manager.add_movie(movie)
    return redirect(url_for('get_movies', user_id=user_id))


if __name__ == '__main__':
    app.run()
