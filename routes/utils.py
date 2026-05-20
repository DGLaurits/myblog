from functools import wraps

from flask import redirect, session, url_for


def is_admin():
    return 'admin' in session and session['admin']


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        return redirect(url_for('blog.index'))
    return wrap
