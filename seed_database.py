"""Script to seed database."""

import os
# This is a module from Python’s standard library.
# It contains code related to working with your computer’s operating system.
# JEM: Needed to open files, delete files...
import json
# So we can load the data in data/movies.json.
from random import choice, randint
# choice is a function that takes in a list and returns a random element in the list. 
# randint will return a random number within a certain range. 
# You’ll use both to generate fake users and ratings
from datetime import datetime
# Use datetime.strptime to turn a string into a Python datetime object.

import crud
import model
import server
# These are all files that we wrote in this project.

os.system("dropdb ratings")  # This is just like:  $ dropdb ratings
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()
"""Remember — we imported model and server instead of importing individual functions.
If we had written from model import db, we'd be able to access db.  (on line 17)
However, since it's just import model, you have to go through model before you can access db.
"""

SEED_USERS = 20
SEED_RATINGS = 20

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
"""
movie_data looks like this: [{'overview': 'The near future, [...] search of the unknown.',
  'poster_path': 'https://image.tmdb.org/t/p/original//xBHvZcjRiWyobQ9kxBhO6B2dtRI.jpg',
  'release_date': '2019-09-20',
  'title': 'Ad Astra'}, ... ]
"""


# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    """ Example movie:
    {
        "overview": "Based on the global blockbuster videogame franchise from Sega, Sonic the Hedgehog tells the story of the world\u2019s speediest hedgehog as he embraces his new home on Earth. In this live-action adventure comedy, Sonic and his new best friend team up to defend the planet from the evil genius Dr. Robotnik and his plans for world domination.",
        "poster_path": "https://image.tmdb.org/t/p/original//aQvJ5WPzZgYVDrxLX4R6cLJCEaQ.jpg",
        "release_date": "2020-02-14",
        "title": "Sonic the Hedgehog"
    },
    """
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title, overview, poster_path = (
        movie['title'], movie['overview'],movie['poster_path'])

    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    # "2020-02-14" = "%Y-%m-%d"
    """ From Datetime formatting Cheat Sheet: https://strftime.org
    %d	08	Day of the month as a zero-padded decimal number.
    %m	09	Month as a zero-padded decimal number.
    %y	13	Year without century as a zero-padded decimal number.
    %Y	2013	Year with century as a decimal number.
    """


    one_movie_instance = crud.create_movie(title, overview, release_date, poster_path)
    # TODO: create a movie here and append it to movies_in_db
    """ Remember, we did this in crud.py:
    movie_1 =create_movie(title = 'Frozen', overview = 'Elsa and Anna have fun in the snow.', poster_path='https://movieposters2.com/images/1650527-b.jpg')
    >> db.session.add(movie_1)
    >> db.session.commit()  
    
    If you want to add a list of objects, you can use db.session.add_all().
    """

    # Populate list defined on line 43. We'll use it later to select a random movie from:
    movies_in_db.append(one_movie_instance)

model.db.session.add_all(movies_in_db)
model.db.session.commit() 

"""
Finally, we'll generate 10 users. One problem — each user needs a unique email address. 
A super easy (albeit not very exciting) way to do this is just to loop over a range of 
numbers and use those numbers to generate the emails (they may be boring but they're 
definitely unique!). After creating the user, you'll need to generate 10 fake ratings 
for that user.
"""

for n in range(SEED_USERS):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    one_user_instance = crud.create_user(email, password)
    model.db.session.add(one_user_instance)
    
    ratings_list = []
    for z in range(SEED_RATINGS):
        one_random_movie_instance = choice(movies_in_db)
        one_rating_instance = crud.create_rating(
            one_user_instance, one_random_movie_instance, randint(0, 5))
        ratings_list.append(one_rating_instance)
    
    model.db.session.add_all(ratings_list)
    model.db.session.commit()

    """
    >> rating = Rating.query.first()
    2022-01-09 00:53:25,102 INFO sqlalchemy.engine.Engine SELECT ratings.rating_id AS ratings_rating_id, ratings.score AS ratings_score, ratings.movie_id AS ratings_movie_id, ratings.user_id AS ratings_user_id 
    FROM ratings 
    LIMIT %(param_1)s
    2022-01-09 00:53:25,102 INFO sqlalchemy.engine.Engine [cached since 179.4s ago] {'param_1': 1}
    >> rating.score
    0
    >> rating.movie_id
    76

    >> rating = Rating.query.first()
    2022-01-09 01:04:29,498 INFO sqlalchemy.engine.Engine SELECT ratings.rating_id AS ratings_rating_id, ratings.score AS ratings_score, ratings.movie_id AS ratings_movie_id, ratings.user_id AS ratings_user_id 
    FROM ratings 
    LIMIT %(param_1)s
    2022-01-09 01:04:29,498 INFO sqlalchemy.engine.Engine [cached since 844.6s ago] {'param_1': 1}
    >> rating.user
    user_id: 1
    email: user0@test.com

    >> rating.movie
    2022-01-09 01:04:43,762 INFO sqlalchemy.engine.Engine SELECT movies.movie_id AS movies_movie_id, movies.title AS movies_title, movies.overview AS movies_overview, movies.release_date AS movies_release_date, movies.poster_path AS movies_poster_path 
    FROM movies 
    WHERE movies.movie_id = %(pk_1)s
    2022-01-09 01:04:43,763 INFO sqlalchemy.engine.Engine [generated in 0.00036s] {'pk_1': 76}
    movie_id: 76
    title: The Hunt
    overview: Twelve strangers wake up in a clearing. They don't know where they are—or how they got there. In the shadow of a dark internet conspiracy theory, ruthless elitists gather at a remote location to hunt humans for sport. But their master plan is about to be derailed when one of the hunted turns the tables on her pursuers.            
    release_date: 2020-03-13 00:00:00
    poster path: https://image.tmdb.org/t/p/original//wxPhn4ef1EAo5njxwBkAEVrlJJG.jpg

    >> for user_rating in rating.user.ratings:
    .. print(user_rating.score)
    File "<stdin>", line 2
        print(user_rating.score)
        ^
    IndentationError: expected an indented block
    >> for user_rating in rating.user.ratings:
    ..     print(user_rating.score)
    .. 
    0
    2
    3
    3
    2
    0
    3
    4
    5
    0
    >> 
    """
    