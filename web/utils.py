import uuid
import jwt

from flask import request, redirect
from functools import wraps
from web.config import *
from web.models.user import *

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def encode_token(user):
    return jwt.encode({'id': user.id, 'email': user.email, 'roll': gen_uuid()}, SECRET, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])['id']

def requires_auth():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                try:
                    decoded = decode_token(request.cookies['jwt'])
                except Exception as e:
                    return redirect('/login?redirect='+request.url)
                user = User.query.filter_by(id=decoded).first()
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                return redirect('/login')

        return decorated
    return decorator