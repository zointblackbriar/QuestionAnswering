from flask import current_app, abort, request
from functools import wraps

from .config import DEFAULT_CONFIG

import jwt

class JWT:
    def __init__(self, app=None):
        self.auth_handler = None
        self.unauthorized = None

        if app is None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in DEFAULT_CONFIG.items():
            app.config.setdefault(k ,v)

        app.config.setdefault("JWT_SECRET_KEY", app.config["SECRET_KEY"])

        app.extensions['jwt'] = self

    def unauthorized_handler(self, callback):
        self.unauthorized = callback
        return callback

def login_required(func):

        @wraps(func)
        def decorator(*args, **kwargs):
            jwt_login = current_app.extensions['jwt']

            token = request.cookies.get(current_app.config["JWT_COOKIE_NAME"])

            #token does not exist
            if token is None:
                if jwt_login.unauthiruzed is None:
                    abort(501)
                return jwt_login.unauthorized()

            try:
                jwt_token = jwt.decode(token, current_app.config["JWT_CONFIG_KEY"], algorithms=[current_app.config['HASH_ALGORITHM']])
            except jwt.exceptions.DecodeError:
                if jwt_login.unauthorized is None:
                    abort(501)
                return jwt_login.unauthorized()

            return func(*args, **kwargs)
        return decorator
