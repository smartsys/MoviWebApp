from models import db, User, Movie


class DataManager():
    """CRUD operations for users and their favorite movies."""

    def create_user(self, name):
        """Create a new user."""
        db.session.add(User(name=name))
        db.session.commit()

    def get_users(self):
        """Return a list of all users."""
        return db.session.execute(db.select(User)).scalars().all()

    def get_movies(self, user_id):
        """Return a list of all movies of a user."""
        return db.session.execute(
            db.select(Movie).filter_by(user_id=user_id)
        ).scalars().all()

    def add_movie(self, movie):
        """Add a new movie to a user's favorites."""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie."""
        movie = db.session.get(Movie, movie_id)
        movie.name = new_title
        db.session.commit()

    def delete_movie(self, movie_id):
        """Delete a movie from a user's favorites."""
        movie = db.session.get(Movie, movie_id)
        db.session.delete(movie)
        db.session.commit()
