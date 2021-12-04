from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, response
from django.views.decorators.csrf import csrf_exempt
import jwt
from .models import User
import json
from django.utils import timezone
import os
import bcrypt
from django.core import serializers
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@csrf_exempt
# @swaggger_auto_schema document
# https://drf-yasg.readthedocs.io/en/stable/drf_yasg.html#drf_yasg.utils.swagger_auto_schema
# drf_yasgs.openapi document
# https://drf-yasg.readthedocs.io/en/stable/drf_yasg.html#module-drf_yasg.openapi
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign up",
    operation_description="sign up with email, password",
    method="post",
    manual_parameters=[
        openapi.Parameter("email", openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, default="abcde@gmail.com", description="email"),
        openapi.Parameter("password", openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, default="qwerasdf", description="password"),
    ],
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: success)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: user signed up)")
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: user already exists)")
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: internal server error)")
            },
        )
    },
    deprecated=False
)
@api_view(["POST"])
@parser_classes([FormParser])
def signup(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]

            is_user = User.objects.filter(email=email).exists()
            if is_user:
                data = { "status": "error", "message": "user already exists" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode("utf-8"), salt)
            user = User(email=email, password=hash.decode("utf-8"), created_at=timezone.now())
            user.save()
            data = { "status": "success", "message": "user signed up" }
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign in",
    operation_description="sign in with email, password",
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, require=True, default="abcde@gmail.com", description="email"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, require=True, default="qwerasdf", description="password"),
        },
    ),
    responses={
        200: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "user signed in",
                    "access_token": "access token"
                }
            },
        ),
        400: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "password is invalid"
                }
            },
        ),
        500: openapi.Response(
            description="sigin success",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "error message"
                }
            },
        )
    },
    deprecated=False
)
@api_view(["POST"])
def signin(request):
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            email = body["email"]
            password = body["password"]

            user = User.objects.filter(email=email)
            is_user = user.exists()

            if not is_user:
                data = { "status": "error", "message": "user does not exist" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            hashed = user.values("password").first()["password"]
            is_match = bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
            if not is_match:
                data = { "status": "error", "message": "password is invalid" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
            access_token = jwt.encode(
                {
                    "email": email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(days=14)
                },
                JWT_SECRET_KEY,
                algorithm="HS256"
            )

            data = {
                "status": "success",
                "message": "user signed in",
                "access_token": access_token
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

@swagger_auto_schema(
    method="get",
    operation_summary="find all users",
    operation_description="find all users' email and created_at",
    tags=["auth"],
    responses={
        200: "success",
        500: "internal server error"
    },
    deprecated=False
)
@api_view(["GET"])
def users(request):
    try:
        if request.method == "GET":
            case = 3
            if case == 1:
                # queryest -> json #1
                users = json.loads(serializers.serialize("json", User.objects.all()))
                data = {"status": "success", "message": "found users",  "data": users}
                return HttpResponse(json.dumps(data), content_type="application/json")
            elif case == 2:
                # queryest -> json #2
                # values document
                # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#values
                users = User.objects.all().values("email")
                data = { "status": "success", "message": "found users",  "data": list(users) }
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                # queryest -> json #3
                users = [{
                    "email": user["email"],
                    "created_at": user["created_at"].strftime("%Y-%m-%d")
                } for user in User.objects.all().values()]
                data = { "status": "success", "message": "found users",  "data": users }
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="change password",
    operation_description="change with new password",
    method="patch",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["current_password", "new_password"],
        properties={
            "current_password": openapi.Schema(type=openapi.TYPE_STRING, require=True, default="qwerasdf", description="current password"),
            "new_password": openapi.Schema(type=openapi.TYPE_STRING, require=True, default="qwerasdf1", description="new password"),
        },
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: success)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: changed password)")
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: user does not exist, password is invalid, password is same")
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: internal server error)")
            },
        )
    },
    deprecated=False
)
@api_view(["PATCH"])
def password(request):
    try:
        if request.method == "PATCH":
            email = request.user_info["email"]
            body = json.loads(request.body)
            current_password = body["current_password"]
            new_password = body["new_password"]

            # get으로 바꾸기
            user = User.objects.filter(email=email)
            is_user = user.exists()
            if not is_user:
                data = { "status": "error", "message": "user does not exist" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            hashed = user.values("password").first()["password"]
            is_match = bcrypt.checkpw(current_password.encode("utf-8"), hashed.encode("utf-8"))
            if not is_match:
                data = { "status": "error", "message": "password is invalid" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            hashed = user.values("password").first()["password"]
            is_match = bcrypt.checkpw(new_password.encode("utf-8"), hashed.encode("utf-8"))
            if is_match:
                data = { "status": "error", "message": "password is same" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(new_password.encode("utf-8"), salt)
            user = User.objects.get(email=email)
            user.password = hash.decode("utf-8")
            user.save()

            data = {
                "status": "success",
                "message": "password changed",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign out",
    operation_description="sign out with password",
    method="delete",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        require=["password"],
        properties={
            "password": openapi.Schema(type=openapi.TYPE_STRING, require=True, default="qwerasdf", description="password")
        },
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: success)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: user signed out)")
            },
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: user does not exist, password is invalid")
            },
        ),
        500: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING, description="status (e.g: error)"),
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="message (e.g: internal server error)")
            },
        )
    },
    deprecated=False
)
@api_view(["DELETE"])
def signout(request):
    # token에서 정보얻어오는걸로 바꾸기
    try:
        if request.method == "DELETE":
            email = request.user_info["email"]
            body = json.loads(request.body)
            password = body["password"]

            # get으로 바꾸기
            user = User.objects.filter(email=email)
            is_user = user.exists()
            if not is_user:
                data = { "status": "error", "message": "user does not exist" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            hashed = user.values("password").first()["password"]
            is_match = bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
            if not is_match:
                data = { "status": "error", "message": "password is invalid" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            user = User.objects.get(email=email)
            user.delete()

            data = {
                "status": "success",
                "message": "user signed out",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

### social signup / login
### admin (settings.py)
### map (class view, postgresql gis, jwt)
### refresh token (redis)
### test code
### lint
### docker
### django rest frame work
### serializer
### function middleware
### class middleware (map, response formatting)
### swagger authentication
### swagger ""comment