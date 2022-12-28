from flask import Blueprint, render_template, flash, redirect
from generic_views import ListView, DetailView
from models import Cafe, City, db
from cafe.forms import AddCafeForm


cafes = Blueprint("cafes", __name__)

cafes.add_url_rule(
    "/cafes",
    view_func=ListView.as_view("cafe_list", Cafe),
)

cafes.add_url_rule(
    "/cafes/<int:id>",
    view_func=DetailView.as_view("cafe_detail", Cafe),
)


@cafes.route("/cafes/add", methods=["POST", "GET"])
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
            image_url=image_url,
        )
        db.session.add(new_cafe)
        db.session.commit()

        flash(f"{new_cafe.name} added.", "success")

        return redirect(f"/cafes/{new_cafe.id}")
    else:
        return render_template("cafe/add-form.html", form=form)


@cafes.route("/cafes/<int:cafe_id>/edit", methods=["POST", "GET"])
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

        flash(f"{cafe.name} edited.", "success")

        return redirect(f"/cafes/{cafe.id}")
    else:
        return render_template(
            "cafe/edit-form.html",
            form=form,
        )
