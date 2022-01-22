from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseServerError
import json
from .utils import decode_bearer_token
import re

# function middleware
def check_access_token_middleware(get_response):
    PATH = ("/api/auth/password/", "/api/auth/delete/")

    def middleware(request):
        try:
            # before view
            if request.path in PATH:
                # https://docs.djangoproject.com/en/3.2/ref/request-response/#httprequest-objects
                access_token = request.headers.get("AUTHORIZATION")

                if not access_token:
                    raise PermissionDenied("no authorization token")

                decode = decode_bearer_token(access_token)
                request.user_info = {"email": decode["email"]}

            response = get_response(request)

            # after view
            return response
        except PermissionDenied as e:
            data = {"status": "error", "message": str(e)}
            return HttpResponse(
                json.dumps(data), content_type="application/json", status=401
            )
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return HttpResponseServerError(
                json.dumps(data), content_type="application/json"
            )

    return middleware


# class middleware
class CheckAccessTokenMiddleWare:
    PATH = (re.compile(r"^/api/map/sggs/$"), re.compile(r"^/api/map/sggs"))

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # before view
            matches = [p.match(request.path) for p in self.PATH]

            if any(matches):
                access_token = request.headers.get("AUTHORIZATION")

                if not access_token:
                    raise PermissionDenied("no authorization token")

                decode = decode_bearer_token(access_token)
                request.user_info = {"email": decode["email"]}

            response = self.get_response(request)

            # after view
            return response
        except PermissionDenied as e:
            data = {"status": "error", "message": str(e)}
            return HttpResponse(
                json.dumps(data), content_type="application/json", status=401
            )
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return HttpResponseServerError(
                json.dumps(data), content_type="application/json"
            )
