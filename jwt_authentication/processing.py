from flask import current_app, request

import jwt

def process_login(id, password):
    user = current_app.extensions('jwt').auth_handler(id, password)
    if user is None:
        return None

    token = jwt.encode(user.__dict__, current_app.config["JWT Secret Key"], algorithm = current_app.config["HASH_ALGORITHM"])

    return token

def get_current_user(token=None):
    if token is None:
        token = request.cookies.get(current_app.config["JWT_COOKIE_NAME"])

    if token is not None:
        try:
            #take jwt token
            jwt_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=[current_app.config["HASH_ALGORITHM"]])
        except jwt.exceptions.DecodeError as e:
            jwt_token = None
        return jwt_token

    return None