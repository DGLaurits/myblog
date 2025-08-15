from flask import session
from functools import wraps

def is_admin():
    return 'admin' in session and session['admin']

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        else:
            return "NOT LOGGED IN"
    return wrap