"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user.
    
    Tested with:
    (venv) 🐳 hackbright@e8ef6377922f:~/src/lab29-ratings-v2 (main) $ python3 -i crud.py
    Connected to the db!
    >> user_1 =create_user('abcd@gmail.com','abcd')
    >> user_1
    user_id: None
    email: abcd@gmail.com

    >> db.session.add(user_1)
    >> db.session.commit()
    2022-01-08 23:19:06,903 INFO sqlalchemy.engine.Engine select version()
    2022-01-08 23:19:06,903 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:19:06,905 INFO sqlalchemy.engine.Engine select current_schema()
    2022-01-08 23:19:06,905 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:19:06,906 INFO sqlalchemy.engine.Engine show standard_conforming_strings
    2022-01-08 23:19:06,906 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:19:06,908 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-01-08 23:19:06,914 INFO sqlalchemy.engine.Engine INSERT INTO users (email, password) VALUES (%(email)s, %(password)s) RETURNING users.user_id
    2022-01-08 23:19:06,914 INFO sqlalchemy.engine.Engine [generated in 0.00080s] {'email': 'abcd@gmail.com', 'password': 'abcd'}
    2022-01-08 23:19:06,917 INFO sqlalchemy.engine.Engine COMMIT
    >> user_1
    2022-01-08 23:19:15,104 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-01-08 23:19:15,107 INFO sqlalchemy.engine.Engine SELECT users.user_id AS users_user_id, users.email AS users_email, users.password AS users_password 
    FROM users 
    WHERE users.user_id = %(pk_1)s
    2022-01-08 23:19:15,107 INFO sqlalchemy.engine.Engine [generated in 0.00021s] {'pk_1': 2}
    user_id: 2
    email: abcd@gmail.com

    # Can't add incomplete entries per our design:
    >> user_2 =create_user('abcd@gmail.com')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: create_user() missing 1 required positional argument: 'password'
    >> user_2 =create_user(password='123d')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: create_user() missing 1 required positional argument: 'email'
    >> 
    """

    user = User(email=email, password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)
    
def create_movie(title, overview, release_date=None, poster_path=None):
    """Create and return a new movie.
    
    From model.py:
    movie_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable = False)  # overview will contain spaces so, db.Text
    release_date = db.Column(db.DateTime)  # 2022-01-08 20:25:09.259450
    poster_path = db.Column(db.String)

    Tested with:
    (venv) 🐳 hackbright@e8ef6377922f:~/src/lab29-ratings-v2 (main) $ python3 -i crud.py
    Connected to the db!
    >> movie_1 =create_movie(title = 'Frozen', overview = 'Elsa and Anna have fun in the snow.', poster_path='https://movieposters2.com/images/1650527-b.jpg')
    >> db.session.add(movie_1)
    >> db.session.commit()
    2022-01-08 23:35:36,781 INFO sqlalchemy.engine.Engine select version()
    2022-01-08 23:35:36,781 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:35:36,782 INFO sqlalchemy.engine.Engine select current_schema()
    2022-01-08 23:35:36,783 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:35:36,784 INFO sqlalchemy.engine.Engine show standard_conforming_strings
    2022-01-08 23:35:36,784 INFO sqlalchemy.engine.Engine [raw sql] {}
    2022-01-08 23:35:36,787 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-01-08 23:35:36,790 INFO sqlalchemy.engine.Engine INSERT INTO movies (title, overview, release_date, poster_path) VALUES (%(title)s, %(overview)s, %(release_date)s, %(poster_path)s) RETURNING movies.movie_id
    2022-01-08 23:35:36,790 INFO sqlalchemy.engine.Engine [generated in 0.00023s] {'title': 'Frozen', 'overview': 'Elsa and Anna have fun in the snow.', 'release_date': None, 'poster_path': 'https://movieposters2.com/images/1650527-b.jpg'}
    2022-01-08 23:35:36,793 INFO sqlalchemy.engine.Engine COMMIT
    >> movie_1
    2022-01-08 23:36:08,968 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-01-08 23:36:08,971 INFO sqlalchemy.engine.Engine SELECT movies.movie_id AS movies_movie_id, movies.title AS movies_title, movies.overview AS movies_overview, movies.release_date AS movies_release_date, movies.poster_path AS movies_poster_path 
    FROM movies 
    WHERE movies.movie_id = %(pk_1)s
    2022-01-08 23:36:08,971 INFO sqlalchemy.engine.Engine [generated in 0.00025s] {'pk_1': 2}
    movie_id: 2
    title: Frozen
    overview: Elsa and Anna have fun in the snow.            
    release_date: None
    poster path: https://movieposters2.com/images/1650527-b.jpg

    >>
    """

    movie = Movie(title = title, overview = overview, \
        release_date = release_date, poster_path = poster_path)

    return movie
    

def get_movies():
    """Return all movies."""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return one movie."""
    
    return Movie.query.get(movie_id)


def create_rating(user_instance, movie_instance, score: int):
    """Create and return a new rating.
    
    Per instructions:
    "This function should take in a User instance, Movie instance, and an integer (for the rating's score).
    Your function should not work with primary keys directly."

    From model.py:
    rating_id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


    Tested with: 
    >> rating1 = create_rating(db.session.query(User).first(), db.session.query(Movie).first(), 5)
    2022-01-08 23:52:56,146 INFO sqlalchemy.engine.Engine SELECT users.user_id AS users_user_id, users.email AS users_email, users.password AS users_password 
    FROM users 
    LIMIT %(param_1)s
    2022-01-08 23:52:56,146 INFO sqlalchemy.engine.Engine [cached since 154.9s ago] {'param_1': 1}
    2022-01-08 23:52:56,149 INFO sqlalchemy.engine.Engine SELECT movies.movie_id AS movies_movie_id, movies.title AS movies_title, movies.overview AS movies_overview, movies.release_date AS movies_release_date, movies.poster_path AS movies_poster_path 
    FROM movies 
    LIMIT %(param_1)s
    2022-01-08 23:52:56,149 INFO sqlalchemy.engine.Engine [generated in 0.00028s] {'param_1': 1}
    >> db.session.add(rating1)
    >> db.session.commit()
    2022-01-08 23:53:53,481 INFO sqlalchemy.engine.Engine INSERT INTO ratings (score, movie_id, user_id) VALUES (%(score)s, %(movie_id)s, %(user_id)s) RETURNING ratings.rating_id
    2022-01-08 23:53:53,482 INFO sqlalchemy.engine.Engine [generated in 0.00071s] {'score': 5, 'movie_id': 1, 'user_id': 1}
    2022-01-08 23:53:53,484 INFO sqlalchemy.engine.Engine COMMIT
    >> rating1
    2022-01-08 23:54:24,737 INFO sqlalchemy.engine.Engine BEGIN (implicit)
    2022-01-08 23:54:24,739 INFO sqlalchemy.engine.Engine SELECT ratings.rating_id AS ratings_rating_id, ratings.score AS ratings_score, ratings.movie_id AS ratings_movie_id, ratings.user_id AS ratings_user_id 
    FROM ratings 
    WHERE ratings.rating_id = %(pk_1)s
    2022-01-08 23:54:24,739 INFO sqlalchemy.engine.Engine [generated in 0.00047s] {'pk_1': 2}
    rating_id: 2
    score: 5
                movie_id: 1
    user_id: 1

    >>
    """

    rating = Rating(user = user_instance, movie = movie_instance, score = score)

    return rating
    
if __name__ == '__main__':
    """Will connect you to the database when you run crud.py interactively"""
    from server import app
    connect_to_db(app)

