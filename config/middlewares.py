from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseServerError
import json
from .utils import decode_bearer_token

# function middleware
def check_access_token_middleware(get_response):
    def middleware(request):
        try:
            # before view
            if request.path == "/api/auth/password/" and "/api/auth/delete/":
                access_token = request.headers.get("AUTHORIZATION")

                if not access_token: raise PermissionDenied("no authorization token")

                decode = decode_bearer_token(access_token)
                request.user_info = { "email" : decode["email"] }

            response = get_response(request)
            # after view
            return response
        except PermissionDenied as e:
            data = { "status": "error", "message": str(e) }
            return HttpResponse(json.dumps(data), content_type="application/json", status=401)
        except Exception as e:
            data = { "status": "error", "message": str(e) }
            return HttpResponseServerError(json.dumps(data), content_type="application/json")
    return middleware
