from flask_wtf import FlaskForm
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


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional(), DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL", validators=[Optional(), URL()])


class UserLoginForm(FlaskForm):
    """Form for logging in users."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])

class ProfileEditForm(FlaskForm):
    """Form for editing profile."""

    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional(), DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    image_url = StringField("(Optional) Image URL", validators=[Optional()]) #URL()
