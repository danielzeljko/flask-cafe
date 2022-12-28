from functools import wraps
from flask import g, request, redirect, url_for, flash


def login_required(func):
    """Login decorator with url next support"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash("You need to login to access this page.", "danger")
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)

    return decorated_function
