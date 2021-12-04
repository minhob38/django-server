import os
from django.core.exceptions import PermissionDenied
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

def decode_bearer_token(bearer_token):
    try:
        token = bearer_token[len("bearer "):]
        decode = jwt.decode(token, JWT_SECRET_KEY, algorithms="HS256")
    except DecodeError:
        raise PermissionDenied("token invalid")
    except ExpiredSignatureError:
        raise PermissionDenied("token expired")
    except Exception as e:
        print(type(e))
    return decode