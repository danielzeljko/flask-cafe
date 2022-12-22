from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, URLField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, URL, Optional, AnyOf, DataRequired

"""Forms for Flask Cafe."""


class AddCafeForm(FlaskForm):
    """Form for adding cafes."""

    name = StringField("Name", validators=[DataRequired()])

    description = TextAreaField("Description", validators=[Optional(), DataRequired()])

    url = URLField("URL", validators=[Optional(), URL()])

    address = StringField("Address", validators=[DataRequired()])

    city_code = SelectField(
        "City",
        # choices=[
        #     ("baby", "Baby"),
        #     ("young", "Young"),
        #     ("adult", "Adult"),
        #     ("senior", "Senior"),
        # ],
        validators=[DataRequired()],
    )
