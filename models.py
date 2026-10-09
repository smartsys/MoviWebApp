from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user with a list of favorite movies."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Return a readable representation of the user."""
        return f"User(id={self.id}, name={self.name!r})"


class Movie(db.Model):
    """A favorite movie belonging to a user."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """Return a readable representation of the movie."""
        return f"Movie(id={self.id}, name={self.name!r}, year={self.year})"
