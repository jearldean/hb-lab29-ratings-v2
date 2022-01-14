"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def homepage():
    """Display homepage."""

    return render_template('homepage.html')

    
@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    if not crud.does_this_user_exist_already(email):
        crud.create_user(email, password)
        flash("Account created! Please log in.")
    else:
        flash("This user already exists! Please try again")
    
    return redirect("/")


@app.route("/login", methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")

    if crud.does_the_password_match(email, password):
        flash(f"Thanks for being a MoveeBuff™, {email}! Help us by rating some movies!")

        # Override on each new login:
        session["user_email"] = email
        
        return redirect("/movies")
    else:
        flash("Password mismatch! Please try again")
        return redirect(request.referrer)


@app.route("/rate", methods=["POST"])
def rate_movie():

    rating = request.form.get("rating")  # Any form reply back is a string.

    nope_msg = "Please try again with a number from 0-5."
    try:
        rating = int(rating)  # Coerce to int.
        if rating not in range(6):
            flash(nope_msg)
            return redirect(request.referrer)
    except ValueError:
        flash(nope_msg)
        return redirect(request.referrer)

    user_email = session["user_email"]
    user = crud.get_user_by_email(user_email)
    movie = crud.get_movie_by_id(session["movie_id"])

    """ 3 things can happen here:
    1. New rating -> add new rating
    2. old_score is the same as new_score. No action, flash message.
    3. Rating exists already and is new -> update.
    """
    if crud.does_this_rating_exist_already(user, movie):
        old_score = crud.get_score_for_existing_rating(user, movie)
        if old_score == rating:
            flash(f"No change to your previous rating of {rating}.")
        else:
            flash(f"Updating your rating from {old_score} to {rating}.")
            crud.update_rating(user, movie, new_score=rating)
    else:
        crud.create_rating(user, movie, score=rating)
        flash(f"Thank you for your rating of {rating} for {movie.title}, {user_email}.")

    return redirect(request.referrer)

    
@app.route("/movies")
def all_movies():
    """View all movies."""
    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route("/movies/<movie_id>")
def one_movie(movie_id):
    """View one movie."""

    movie_id = int(movie_id)

    movie = crud.get_movie_by_id(movie_id)

    # Put movie_id in session here: (override on each new page load)
    session["movie_id"] = movie_id

    average_rating, count_scores = crud.get_movie_rating(movie)

    user = crud.get_user_by_email(session["user_email"])
    if crud.does_this_rating_exist_already(user, movie):
        old_score = crud.get_score_for_existing_rating(user, movie)
        flash(f"Your rating for {movie.title} is a {old_score}.")
    else:
        flash(f"You have not previously rated this movie.")

    return render_template('movie_details.html', movie=movie, rating_average=average_rating, num_users=count_scores)


@app.route("/users")
def all_users():
    """View all users."""
    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route("/user/<user_id>")
def one_user(user_id):
    """View one user."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = False

    app.run(host="0.0.0.0", debug=True)


# from flask import request, session, flash, redirect

# @app.route('/handle-login', methods=['POST'])
# def handle_login():
#     """Log user into application."""

#     username = request.form['username']
#     password = request.form['password']

#     if password == 'let-me-in':   # FIXME
#         session['current_user'] = username
#         flash(f'Logged in as {username}')
#         return redirect('/')

#     else:
#         flash('Wrong password!')
#         return redirect('/login')