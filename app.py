"""Flask App for Flask Cafe."""

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os
from sqlalchemy.exc import IntegrityError

from decorators import login_required

from models import db, connect_db, User
from forms import UserAddForm, UserLoginForm, ProfileEditForm

from cafe.views import cafes


app = Flask(__name__)
app.register_blueprint(cafes)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flaskcafe"
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("auth/signup-form.html", form=form)

        do_login(user)

        flash("You are signed up and logged in.")

        return redirect("/")

    else:
        return render_template("auth/signup-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage or next url on success."""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        next_url = request.form.get("next")
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            if next_url:
                return redirect(next_url)
            return redirect("/")
        else:
            flash("Invalid credentials.", "danger")

    return render_template("auth/login-form.html", form=form)


@app.post("/logout")
@login_required
def logout():
    """Handle logout of user and redirect to homepage."""

    flash("You should have successfully logged out.")
    do_logout()

    return redirect("/")


#######################################
# homepage


@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")



# profiles


@app.get("/profile")
@login_required
def show_profile():
    """Show profile page."""

    user = User.query.get(g.user.id)
    return render_template("profile/detail.html", user=user)


@app.route("/profile/edit", methods=["POST", "GET"])
@login_required
def edit_profile():
    """Edit profile page."""

    user = User.query.get(g.user.id)
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("Profile edited.")
        return redirect("/profile")
    else:
        return render_template("profile/edit-form.html", form=form, user=user)
