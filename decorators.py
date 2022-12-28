from functools import wraps
from flask import g, request, redirect, url_for


def login_required(func):
    """Login decorator with url next support"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)

    return decorated_function
