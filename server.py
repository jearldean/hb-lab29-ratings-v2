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
        flash("Logged in! Please rate some movies!")

        # Establish a session only after a successful login:
        if "session_details" not in session:
            session["session_details"] = {}

        # Override on each new login:
        session["session_details"]["user_email"] = email
        # This failed when we didn't initialize the movie_id key:
        session["session_details"]["movie_id"] = None
        
        return redirect("/movies")
    else:
        flash("Password mismatch! Please try again")
        return redirect("/")


@app.route("/rate", methods=["POST"])
def rate_movie():

    rating = request.form.get("rating")  # Any form reply back is a string.
    try:
        rating = int(rating)  # Coerce to int.
    except TypeError:
        flash("Please try again with a number from 1-5.")

    user_email = session["session_details"]["user_email"]
    user = crud.get_user_by_email(user_email)
    movie = crud.get_movie_by_id(session["session_details"]["movie_id"])

    crud.create_rating(user, movie, score=rating)

    flash("Rate more movies!")
    return redirect("/movies")

    
@app.route("/movies")
def all_movies():
    """View all movies."""
    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route("/movies/<movie_id>")
def one_movie(movie_id):
    """View one movie."""

    movie = crud.get_movie_by_id(movie_id)

    # Put movie_id in session here: (override on each new page load)
    session["session_details"]["movie_id"] = movie_id

    return render_template('movie_details.html', movie=movie)


@app.route("/users")
def all_users():
    """View all users."""
    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route("/user/<user_id>")
def one_user(user_id):
    """View one user."""

    user = crud.get_user_by_id(user_id)
    print(f"I am user_id: {user_id}")

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    connect_to_db(app)
    # DebugToolbarExtension(app)

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