from flask import Blueprint, render_template, flash, redirect, g

# from generic_views import ListView, DetailView
from models import User, db

from user.forms import ProfileEditForm
from decorators import login_required

users = Blueprint("users", __name__)


@users.get("/profile")
@login_required
def show_profile():
    """Show profile page."""

    user = User.query.get(g.user.id)
    return render_template("profile/detail.html", user=user)


@users.route("/profile/edit", methods=["POST", "GET"])
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

