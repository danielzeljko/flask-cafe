"""Flask App for Flask Cafe."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import os

from models import db, connect_db, Cafe, City
from forms import AddCafeForm


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


# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


#######################################
# homepage


@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.get("/cafes")
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by("name").all()

    return render_template(
        "cafe/list.html",
        cafes=cafes,
    )


@app.get("/cafes/<int:cafe_id>")
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        "cafe/detail.html",
        cafe=cafe,
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
        # todo: img url

        new_cafe = Cafe(
            name=name,
            description=description,
            url=url,
            address=address,
            city_code=city_code
        )
        db.session.add(new_cafe)
        db.session.commit()

        flash(f"{new_cafe.name} added.")

        return redirect(f"/cafes/{new_cafe.id}")
    else:
        return render_template("cafe/add-form.html", form=form)
