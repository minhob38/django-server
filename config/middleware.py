import os
import jwt

# function middleware
def check_access_token_middleware(get_response):
    def middleware(request):
        # before view
        access_token = request.META["HTTP_AUTHORIZATION"]
        access_token = access_token[len("bearer "):]
        JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        decode = jwt.decode(access_token, JWT_SECRET_KEY, algorithms="HS256")
        request.user_info = { "email" : decode["email"] }

        response = get_response(request)
        # after view
        return response

    return middleware