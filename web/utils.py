import uuid
import jwt

from flask import request, redirect, abort
from flask_login import current_user
from functools import wraps
from web.config import *
from web.models.user import *


def gen_uuid():
    return str(uuid.uuid4()).replace("-", "")


def encode_token(user):
    return jwt.encode(
        {"id": user.id, "email": user.email, "roll": gen_uuid()},
        SECRET,
        algorithm="HS256",
    )


def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])["id"]


def requires_auth():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "jwt" in request.cookies:
                try:
                    decoded = decode_token(request.cookies["jwt"])
                except Exception:
                    return redirect("/login?redirect=" + request.url)
                user = User.query.filter_by(id=decoded).first()
                f.__globals__["user"] = user
                return f(*args, **kwargs)
            else:
                return redirect("/login")

        return decorated

    return decorator


def permission_required(permission):
    """Restrict a view to users with the given permission."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
