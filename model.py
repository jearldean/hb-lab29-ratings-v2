"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String, nullable = False)
    # ratings = a list of Rating objects

    def __repr__(self):
        return f'user_id: {self.user_id}\nemail: {self.email}\n'

class Movie(db.Model):
    """A movie."""

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable = False)  # overview will contain spaces so, db.Text
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)
    # ratings = a list of Rating objects

    def __repr__(self):
        return f'movie_id: {self.movie_id}\ntitle: {self.title}\noverview: {self.overview}\
            \nrelease_date: {self.release_date}\nposter path: {self.poster_path}\n'

class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
 
    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")
    """Rating.movie and Rating.user both have backrefs to attributes called ratings. 
    This means that SQLAlchemy will automatically create a ratings attribute in User 
    and Movie objects that'll return a list of Ratings.
    """

    def __repr__(self):
        return f'rating_id: {self.rating_id}\nscore: {self.score}\n\
            movie_id: {self.movie_id}\nuser_id: {self.user_id}\n'


"""
View a list of all movies
View the details of one movie
View a list of all users
View the details of one user (a.k.a. the user's profile page)
Create an account
Log in with an account that already exists
Once users have logged in, they'll be able to rate movies between 0-5

Can multiple users rate the same movie? YES
    In other words, how many ratings can a movie have? As many as users.
Can one user rate multiple movies?
    Yes, they should be able to rate as many as they like
How will you associate a rating with a certain user and movie?
    Maybe a ratings table and a movies table and a users table. JOIN



"""




def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
