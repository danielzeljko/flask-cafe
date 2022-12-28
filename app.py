"""Flask App for Flask Cafe."""

from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os
from sqlalchemy.exc import IntegrityError

from generic_views import ListView, DetailView

from models import db, connect_db, Cafe, City, User
from forms import AddCafeForm, UserAddForm, UserLoginForm, ProfileEditForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flaskcafe"
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True

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
    """Handle user login and redirect to homepage on success."""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

    flash("Invalid credentials.", "danger")

    return render_template("auth/login-form.html", form=form)


@app.post("/logout")
def logout():
    """Handle logout of user and redirect to homepage."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    # Note: Added csrf form to g
    # form = g.csrf_form

    # if form.validate_on_submit():
    flash("You should have successfully logged out.")
    do_logout()

    return redirect("/")


#######################################
# homepage


@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes

app.add_url_rule(
    "/cafes",
    view_func=ListView.as_view("cafe_list", Cafe),
)

app.add_url_rule(
    "/cafes/<int:id>",
    view_func=DetailView.as_view("cafe_detail", Cafe)
)


@app.route("/cafes/add", methods=["POST", "GET"])
def cafe_add():
    """Show and handle form for adding a cafe."""

    form = AddCafeForm()
    avail_cities = [(city.code, city.name) for city in City.query.all()]
    form.city_code.choices = avail_cities

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data or None

        new_cafe = Cafe(
            name=name,
            description=description,
            url=url,
            address=address,
            city_code=city_code,
            image_url=image_url
        )
        db.session.add(new_cafe)
        db.session.commit()

        flash(f"{new_cafe.name} added.")

        return redirect(f"/cafes/{new_cafe.id}")
    else:
        return render_template("cafe/add-form.html", form=form)


@app.route("/cafes/<int:cafe_id>/edit", methods=["POST", "GET"])
def cafe_edit(cafe_id):
    """Show and handle form for editing a cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    form = AddCafeForm(obj=cafe)
    avail_cities = [(city.code, city.name) for city in City.query.all()]
    form.city_code.choices = avail_cities
    form.city_code.default = cafe.city_code

    if form.validate_on_submit():
        form.populate_obj(cafe)
        db.session.commit()
        flash(f"{cafe.name} edited.")
        return redirect(f"/cafes/{cafe.id}")
    else:
        return render_template(
            "cafe/edit-form.html",
            form=form,
        )


# profiles

@app.get("/profile")
def show_profile():
    """Show profile page."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(g.user.id)

    return render_template("profile/detail.html", user=user)


@app.route("/profile/edit", methods=["POST", "GET"])
def edit_profile():
    """Edit profile page."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(g.user.id)

    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("Profile edited.")
        return redirect("/profile")
    else:
        return render_template("profile/edit-form.html", form=form, user=user)