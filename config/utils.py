import os
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
import bcrypt

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


def create_token(email):
    token = jwt.encode(
        {
            "email": email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=14),
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )

    return token


def decode_bearer_token(bearer_token):
    try:
        token = bearer_token[len("bearer ") :]
        decode = jwt.decode(token, JWT_SECRET_KEY, algorithms="HS256")
    except DecodeError:
        raise PermissionDenied("token invalid")
    except ExpiredSignatureError:
        raise PermissionDenied("token expired")

    return decode


def create_hash(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    str_hash = hash.decode("utf-8")
    return str_hash


def get_is_match_password(password, hash):
    is_match = bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

    return is_match
