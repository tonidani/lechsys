from functools import wraps


from flask_login import current_user
from flask import flash, redirect, url_for, jsonify
from flask_jwt_extended import get_jwt


# Own role decorator because Flask-login does not implement that :)
def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for i in roles:
                if i not in current_user.show_role():
                    flash('You dont have permissions to see this page', 'error')
                    return redirect(url_for('home'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def blocked_access(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for i in roles:
                if i in current_user.show_role():
                    flash('You dont have permissions to see this page', 'error')
                    return redirect(url_for('home'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def is_logged(f):
    @wraps(f)
    def decorated(*args , **kwargs) :
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return  f(*args, **kwargs)

    return decorated



def token_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == 'admin':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


def token_player_blocked():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims["role"] == 'player':
                return jsonify(msg="Players can not see this!!") , 403
            else:
                return fn(*args, **kwargs)

        return decorator

    return wrapper


