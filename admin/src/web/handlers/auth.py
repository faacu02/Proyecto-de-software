import core.models.User as auth
from functools import wraps
from flask import abort, session


def is_authenticated(session):
    return session.get("user") is not None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            abort(401)
        return f(*args, **kwargs)

    return wrapper


def blocked_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_blocked(session):
            abort(504)
        return f(*args, **kwargs)

    return wrapper


def check(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not check_permission(session, permission):
                abort(403)
            return f(*args, **kwargs)

        return wrapper

    return decorator


def check_permissions(*permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not any(
                check_permission(session, permission) for permission in permissions
            ):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def check_permission(session, permission):
    user_email = session.get("user")
    user = auth.find_user_by_email(user_email)
    permisos = auth.get_permisos(user_email)
    return user is not None and any(permission == permiso.name for permiso in permisos)


def is_blocked(session):
    user_email = session.get("user")
    user = auth.find_user_by_email(user_email)
    return not user.activo
