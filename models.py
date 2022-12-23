"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMG_URL = "/static/images/default-pic.png"


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(25), nullable=False, unique=True)

    admin = db.Column(db.Boolean, nullable=False, default=False)

    email = db.Column(
        db.String(50),
        nullable=False,
    )

    first_name = db.Column(
        db.String(25),
        nullable=False,
    )

    last_name = db.Column(
        db.String(25),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_IMG_URL,
    )

    password = db.Column(db.Text, nullable=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(
        cls,
        username,
        password,
        description,
        first_name,
        last_name,
        email,
        image_url=DEFAULT_IMG_URL,
        admin=False,
    ):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email,
            image_url=image_url,
            description=description,
            admin=admin,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = "cities"

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = "cafes"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey("cities.code"),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref="cafes")

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f"{city.name}, {city.state}"


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
