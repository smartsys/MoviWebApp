from sqlalchemy.exc import SQLAlchemyError

from models import db, User, Movie


class DataManager():
    """CRUD operations for users and their favorite movies."""

    def commit(self):
        """Commit the session and roll it back on database errors."""
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def create_user(self, name):
        """Create a new user."""
        db.session.add(User(name=name))
        self.commit()

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
        self.commit()

    def update_movie(self, movie_id, new_title):
        """Update the title of a movie and return False if it does not exist."""
        movie = db.session.get(Movie, movie_id)
        if movie is None:
            return False
        movie.name = new_title
        self.commit()
        return True

    def delete_movie(self, movie_id):
        """Delete a movie and return False if it does not exist."""
        movie = db.session.get(Movie, movie_id)
        if movie is None:
            return False
        db.session.delete(movie)
        self.commit()
        return True
