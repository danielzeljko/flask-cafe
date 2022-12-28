from flask_wtf import FlaskForm

from wtforms_alchemy import model_form_factory

from models import db, Cafe

from wtforms import (
    StringField,
    SelectField,
    URLField,
    TextAreaField,
)
from wtforms.validators import (
    URL,
    Optional,
    DataRequired,
)

"""Forms for Flask Cafe."""

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class AddCafeForm(ModelForm):
    """Form for adding or editing cafes."""

    name = StringField(
        "Name",
        validators=[DataRequired()],
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), DataRequired()],
    )
    url = URLField(
        "URL",
        validators=[Optional(), URL()],
    )
    address = StringField(
        "Address",
        validators=[DataRequired()],
    )
    city_code = SelectField(
        "City",
        validators=[DataRequired()],
    )
    image_url = StringField(
        "(Optional) Image URL",
        validators=[Optional(), URL()],
    )

    class Meta:
        model = Cafe
