from flask_wtf import FlaskForm

from wtforms_alchemy import model_form_factory

from models import User, db

from wtforms import (
    StringField,
    SelectField,
    PasswordField,
    URLField,
    TextAreaField,
)
from wtforms.validators import (
    URL,
    Optional,
    Length,
    DataRequired,
    Email,
)

"""Forms for Flask Cafe."""

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class AddCafeForm(FlaskForm):
    """Form for adding cafes."""

    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional(), DataRequired()])
    url = URLField("URL", validators=[Optional(), URL()])
    address = StringField("Address", validators=[DataRequired()])
    city_code = SelectField(
        "City",
        validators=[DataRequired()],
    )
    image_url = StringField("(Optional) Image URL", validators=[Optional(), URL()])


class UserAddForm(BaseModelForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional(), DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL", validators=[Optional(), URL()])

    class Meta:
        model = User
        only = [
            "username",
            "first_name",
            "last_name",
            "description",
            "email",
            "password",
            "image_url",
        ]


class UserLoginForm(BaseModelForm):
    """Form for logging in users."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

    class Meta:
        model = User
        only = ["username", "password"]


class ProfileEditForm(BaseModelForm):
    """Form for editing profile."""

    email = StringField("E-mail", validators=[DataRequired(), Email()])

    class Meta:
        model = User
        only = ["first_name", "last_name", "description", "email", "image_url"]
